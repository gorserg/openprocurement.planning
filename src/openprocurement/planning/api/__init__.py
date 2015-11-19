# -*- coding: utf-8 -*-
""" Initialization of new database for external usage (eg Planing API)
"""

from time import sleep

from couchdb.http import ResourceConflict
from schematics.exceptions import ModelValidationError

from openprocurement.api.models import get_now
from openprocurement.api.utils import get_revision_changes, Revision, context_unpack, LOGGER
from openprocurement.planning.api.design import sync_design_plan


def initPlanning(config):
    # scan view in direcory planning/views
    config.scan("openprocurement.planning.api.views")

    # config planning couchdb database
    server = config.registry.couchdb_server  # current database
    db_name = config.registry.db.name  # main database name
    db_name_plan = config.get_settings().get('couchdb.db_name_plan') if config.get_settings().get(
        'couchdb.db_name_plan') else db_name + '_plan'  # planning database name - from config or with '_plan' suffix
    # create additional database if does't exist
    if db_name_plan not in server:
        server.create(db_name_plan)
    db_plan = server[db_name_plan]
    # sync couchdb views
    sync_design_plan(db_plan)
    # add planning database to registry
    config.registry.db_plan = db_plan


def generate_plan_id(ctime, db, server_id=''):
    key = ctime.date().isoformat()
    planIDdoc = 'planID_' + server_id if server_id else 'planID'
    while True:
        try:
            planID = db.get(planIDdoc, {'_id': planIDdoc})
            index = planID.get(key, 1)
            planID[key] = index + 1
            db.save(planID)
        except ResourceConflict:  # pragma: no cover
            pass
        except Exception:  # pragma: no cover
            sleep(1)
        else:
            break
    return 'UA-{:04}-{:02}-{:02}-{:06}{}'.format(ctime.year, ctime.month, ctime.day, index,
                                                 server_id and '-' + server_id)


def save_plan(request):
    plan = request.validated['plan']
    patch = get_revision_changes(plan.serialize("plain"), request.validated['plan_src'])
    plan.revisions.append(Revision({'author': request.authenticated_userid, 'changes': patch, 'rev': plan.rev}))
    old_dateModified = plan.dateModified
    plan.dateModified = get_now()
    try:
        plan.store(request.registry.db_plan)
    except ModelValidationError, e:
        for i in e.message:
            request.errors.add('body', i, e.message[i])
        request.errors.status = 422
    except Exception, e:  # pragma: no cover
        request.errors.add('body', 'data', str(e))
    else:
        LOGGER.info(
            'Saved plan {}: dateModified {} -> {}'.format(plan.id, old_dateModified and old_dateModified.isoformat(),
                                                          plan.dateModified.isoformat()),
            extra=context_unpack(request, {'MESSAGE_ID': 'save_plan'}, {'PLAN_REV': plan.rev}))
        return True


def plan_serialize(plan, fields):
    return dict([(i, j) for i, j in plan.serialize('view').items() if i in fields])
