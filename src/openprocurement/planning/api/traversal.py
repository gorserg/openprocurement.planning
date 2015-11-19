# -*- coding: utf-8 -*-

from pyramid.security import (
    Allow,
    Deny,
    Everyone,
)

from openprocurement.api.utils import error_handler
from openprocurement.planning.api.models import Plan


def get_planning_acl():
    return PlanRoot.__acl__

class PlanRoot(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
        (Deny, 'broker05', 'create_plan'),
        (Allow, Everyone, 'view_plan'),
        (Allow, 'g:brokers', 'create_plan'),
        (Allow, 'g:brokers', 'edit_plan'),
        (Allow, 'g:Administrator', 'edit_plan'),
    ]

    def __init__(self, request):
        self.request = request
        self.db_plan = request.registry.db_plan

def planning_factory(request):
    request.validated['plan_src'] = {}
    root = PlanRoot(request)
    # query containt param plan_id (GET request)
    plan_id = request.matchdict.get('plan_id') if request.matchdict else None
    if plan_id:
        # fill id of Plan
        request.validated['plan_id'] = plan_id
        # find entry in planning database by ID
        plan = Plan.load(root.db_plan, plan_id)
        # plan not found
        if not plan:
            request.errors.add('url', 'plan_id', 'Not Found')
            request.errors.status = 404
            raise error_handler(request.errors)

        plan.__parent__ = root
        request.validated['plan'] = plan
        if request.method != 'GET':
            request.validated['plan_src'] = plan.serialize('plain')
        request.validated['id'] = plan_id
        return plan

    return None