# -*- coding: utf-8 -*-
import unittest
import webtest
import os
from copy import deepcopy
from datetime import datetime, timedelta
from uuid import uuid4
from openprocurement.api import VERSION
from openprocurement.api.tests.base import PrefixedRequestClass

now = datetime.now()
test_plan_data = {
    "tender": {
        "procurementMethod": u"open",
        "tenderPeriod": {
            "startDate": (now + timedelta(days=7)).isoformat()
        }
    },
    "items": [
        {
            "deliveryDate": {
                "endDate": (now + timedelta(days=15)).isoformat()
            },
            "additionalClassifications": [
                {
                    "scheme": u"ДКПП",
                    "id": u"28.29.39-10.00",
                    "description": u"Прилади контролювання маси та прилади контрольні"
                },
                {
                    "scheme": u"КЕКВ",
                    "id": u"123",
                    "description": u"-"
                }
            ],
            "unit": {
                "code": u"KGM",
                "name": u"кг"
            },
            "classification": {
                "scheme": u"CPV",
                "description": u"Роботи з будування пневматичних будівель",
                "id": u"45217000-1"
            },
            "quantity": 760
        }
    ],
    "procuringEntity": {
        "identifier": {
            "scheme": u"UA-EDR",
            "id": u"111983",
            "legalName": u"ДП Державне Уравління Справами"
        },
        "name": u"ДУС"
    },
    "budget": {
        "project": {
            "name": u"proj_name",
            "id": u"proj_id"
        },
        "amount": 10000,
        "amountNet": 12222,
        "currency": u"UAH",
        "id": u"budget_id",
        "description": u"budget_description"
    }
}


class BaseWebTest(unittest.TestCase):
    """Base Web Test to test openprocurement.planning.api.

    It setups the database before each test and delete it after.
    """

    def setUp(self):
        self.app = webtest.TestApp(
            "config:tests.ini", relative_to=os.path.dirname(__file__))
        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('token', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db
        self.db_plan = self.app.app.registry.db_plan

    def tearDown(self):
        del self.couchdb_server[self.db.name]
        del self.couchdb_server[self.db_plan.name]
#
#
# class BaseTenderWebTest(BaseWebTest):
#     initial_data = test_plan_data
#
#     def setUp(self):
#         super(BaseTenderWebTest, self).setUp()
#
#         authorization = self.app.authorization
#         self.app.authorization = ('Basic', ('token', ''))
#         response = self.app.patch_json('/plans/{}'.format(self.tender_id), {'data': self.initial_data})
#         self.app.authorization = authorization
#         self.assertEqual(response.status, '200 OK')
#         self.assertEqual(response.content_type, 'application/json')
#
#     def tearDown(self):
#         super(BaseTenderWebTest, self).tearDown()
