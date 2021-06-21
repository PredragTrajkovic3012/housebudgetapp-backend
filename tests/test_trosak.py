from tests.helper import test_base, test_base_tornado
import users_api as api
import unittest
import users_models
import users_api.user_regiter
import uuid

id_tenant = '00000000-1111-2222-3333-000000000001'
id_user = '00000000-1111-2222-3333-000000000002'

import users_api.trosak as transactions_api
import users_api.transtactions as transactions_api
import users_api.transactiontype as transactiontype_api

'''
user    datum       amount      drescription        balance:

igor    1 apr       +700        plata               700
igor    2 apr       -50         rucak               650
igor    3 apr       -200        racuni              450
igor    3 apr       +180        ispravka greske kod racuna  630
pedja   3 apr       +800        plata               800
milos   3 apr       -50         rucak               -50



            
igor: 630
pedja: 800
milos: -50


'''

import tortoise.timezone



class TestDevel(test_base):

    def test_(self):


        user1 = self.a(users_api.user_regiter.register(id_tenant, "PeraZmaj", "Peraglava123!", "Petar", "Peric", 20000))

        from unittest.mock import patch
        import datetime

        with patch('users_models.models.tz_now',return_value=tortoise.timezone.datetime(2020, 3, 18, 5,0,0)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 200, 'plata')))

        with patch('users_models.models.tz_now', return_value=tortoise.timezone.datetime(2020, 3, 18, 5,0,1)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 20, 'bonus')))

        with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 20, 16)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 2, 'rucak')))

        with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 21, 16)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 1, 'sladoled')))

        with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 22, 16)):
            r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 1000, 'auto')))

        for i in range(4,12):
            with patch('users_models.models.tz_now',return_value=tortoise.timezone.datetime(2020, i, 1, 5,0,0)):
                r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 400, 'plata')))

        #self.flush_db_at_the_end = False



class test_trosak_crud(test_base):

    def test_add(self):
        # self.flush_db_at_the_end = False
        user1 = self.a(users_api.user_regiter.add("PeraZmaj!@", "Peraglava123!", "Petar", "Peric", 20000))

        id_user = user1['id']

        self.assertIn('id', self.a(transactions_api.add_transaction("outcome",id_user, 200, 'Za klopu na praksi')))
        id_trosak = self.a(transactions_api.add_transaction("outcome",id_user, 200,'Za klopu na praksi'))['id']

        user = self.a(users_models.User.filter(id=id_user).get_or_none())
        if not user:
            return {'status': 'error', 'message': 'not-found'}

        user.plati_trosak(id_trosak)

    def test_get_by_id(self):
        user1 = self.a(users_api.user_regiter.add("PeraZmaj!@", "Peraglava123!", "Petar", "Peric", 20000))
        id_user = user1['id']
        res = self.a(transactions_api.add_transaction("outcome",id_user, 200,'Za klopu na praksi'))
        self.assertIn('id', res)
        id_trosak = res['id']
        r = self.a(transactions_api.get(id_trosak))
        print(r)

    def test_get_all(self):
        user1 = self.a(users_api.user_regiter.add("PeraZmaj!@", "Peraglava123!", "Petar", "Peric", 20000))
        id_user = user1['id']
        self.assertEqual(0, len(self.a(transactions_api.get_all(id_user))))
        self.assertIn('id', self.a(transactions_api.add_transaction("outcome",id_user, 200,'Za klopu na praksi')))
        self.assertEqual(1, len(self.a(transactions_api.get_all(id_user))))


    def test_get_avg_of_positive_transaction(self):
        user1 = self.a(users_api.user_regiter.add("PeraZmaj!@", "Peraglava123!", "Petar", "Peric", 20000))
        id_user = user1['id']
        self.assertEqual(0, len(self.a(transactions_api.get_all(id_user))))
        self.assertIn('id', self.a(transactions_api.add_transaction("income",id_user, 200,'Dao deda')))
        self.assertIn('id', self.a(transactions_api.add_transaction("income", id_user, 500, 'Dala baba')))
        self.assertEqual(2, len(self.a(transactions_api.get_all(id_user))))
        print(self.a(transactions_api.get_avg_of_all_positive_transaction(id_user)))



class TestGetDates(test_base):

    def test_mock_date_and_get(self):
        from unittest.mock import patch
        import datetime

        user1 = self.a(users_api.user_regiter.register(id_tenant, "gavradobardecko", "Mir97beo_!", "Gavra", "Gavric", 20000))


        r = self.assertIn('status', self.a(transactiontype_api.setTransactionTypes()))

        self.flush_db_at_the_end = False

        # with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 21, 16)):
        #     r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 10, 'zvake')))
        #
        # with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 3, 22, 16)):
        #     r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 50, 'Metan CNG')))
        #
        # with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 4, 21, 16)):
        #     r = self.assertIn('id', self.a(transactions_api.add_transaction('outcome', user1['id_user'], 10, 'slatis')))
        #
        # with patch('users_models.models.tz_now', return_value=datetime.datetime(2020, 4, 22, 16)):
        #     r = self.assertIn('id',self.a(transactions_api.add_transaction('outcome', user1['id_user'], 50, 'pljeka')))

            # print(self.a(transactions_api.get_all(user1['id_user'],4,2020)))





