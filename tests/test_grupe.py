
import users_models
from tests.helper import test_base
import users_api as api
import unittest

import users_api.user_regiter
import uuid

from unittest.mock import patch
import users_api.transtactions as transactions_api
import datetime
import tortoise.timezone

id_tenant = '00000000-1111-2222-3333-000000000001'
DEFAULT_PASSWORD = "DefaultComplexPassword1._?"



import users_api.grupe as grupe_api

class test_grupe_crud(test_base):


    def test_add(self):
        self.assertIn('id', self.a(grupe_api.add( "Grupa1")))

    def test_get_by_id(self):
        #self.flush_db_at_the_end = False
        res = self.a(grupe_api.add("Grupa1"))
        self.assertIn('id', res)
        id_grupe = res['id']
        #print(id_grupe)
        r = self.a(grupe_api.get(id_grupe))
        self.assertEqual(id_grupe,r['id'])


    def test_add_user_to_group(self):
        res = self.a(grupe_api.add("GrupaPraksa"))
        self.assertIn('id', res)
        id_grupe = res['id']
        res2 = self.a(users_api.user_regiter.add("PeraZmaj!@", "Peraglava123!", "Petar", "Peric", 20000))
        id_user=res2['id']
        print(id_user)
        user = self.a(users_models.User.filter(id=id_user).get_or_none())
        if not user:
            return {'status': 'error', 'message': 'not-found'}

    def test_create_group_add_user(self):
        #self.flush_db_at_the_end = False
        res = self.a(api.register(id_tenant, 'Slobz', DEFAULT_PASSWORD))
        self.assertIsNotNone(res)
        self.assertIn('id_user', res)
        self.assertIn('status', res)
        id_user = res['id_user']
        self.assertEqual('ok', res['status'])
        res2 = self.a(api.grupe.add("Neka Grupa"))
        self.assertIsNotNone(res2)
        self.assertIn('id', res2)
        id_group = res2['id']
        res3 = self.a(api.grupe.get(id_group))

        self.assertIn('id', res3)
        self.assertEqual('Neka Grupa', res3['name'])

        res4 = self.a(api.user_regiter.patch_user_group(id_user, id_group))
        print(id_user)
        print(id_group)
        print(res4)

    def test_group_budget_property(self):
        # self.flush_db_at_the_end = False
        user1 = self.a(users_api.user_regiter.register(id_tenant, "PeraZmaj", "Peraglava123!", "Petar", "Peric", 20000))
        self.assertIsNotNone(user1)
        self.assertIn('id_user', user1)
        id_user = user1['id_user']

        user2 = self.a(users_api.user_regiter.register(id_tenant, "SinDragan", "SinDragan123!", "Sin", "Dragan", 20000))
        self.assertIsNotNone(user2)
        self.assertIn('id_user', user2)
        id_user2 = user2['id_user']
        group = self.a(api.grupe.add("Ujedinjeni pilicari"))
        self.assertIsNotNone(group)
        self.assertIn('id', group)
        id_group = group['id']


        with patch('users_models.models.tz_now',return_value=tortoise.timezone.datetime(2020, 3, 18, 5,0,0)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 200, 'plata')))
        with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 20, 16)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 10, 'rucak')))
        with patch('users_models.models.tz_now',return_value=tortoise.timezone.datetime(2020, 3, 18, 5,0,0)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user2['id_user'], 100, 'plata')))




        res = self.a(api.user_regiter.patch_user_group(id_user, id_group))
        res2= self.a(api.user_regiter.patch_user_group(id_user2, id_group))

        res3=self.a(api.grupe.get_group_budget(id_group))
        print(res3)
        print(id_user)
        print(id_group)
        print(res)
        print(res2)









