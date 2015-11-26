# -*- coding: utf-8 -*-
""" Main function for export module Planing API
"""

from openprocurement.planning.api.traversal import planning_factory, get_planning_acl
from openprocurement.planning.api.utils import init_planning_module


def init_module(config):
    """ Initialization of module (for dynamic invoke from main API)
    :param config: configuration object of main instance
    """
    init_planning_module(config)


def get_factory(request):
    """ Module logic for process request for API
    :param request:
    :return: None - if request not match
    """
    return planning_factory(request)


def get_acl_list():
    """ Access list for current model - for extend default Root acl
    :return: acl collection
    """
    return get_planning_acl()
