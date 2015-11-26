# -*- coding: utf-8 -*-
from openprocurement.api.utils import update_logging_context
from openprocurement.api.validation import validate_data
from openprocurement.planning.api.models import Plan


def validate_plan_data(request):
    update_logging_context(request, {'plan_id': '__new__'})
    return validate_data(request, Plan)


def validate_patch_plan_data(request):
    return validate_data(request, Plan, True)
