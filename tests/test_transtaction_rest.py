import unittest
import json
from tests.helper import test_base_tornado

from tornado.httpclient import AsyncHTTPClient

from tests.test_rest import ID_TENANT
import uuid


class TestTrosakRest(test_base_tornado):

    def setUp(self):
        super().setUp()
        self.api(None, 'POST', '/api/users/register',
                 body={
                     'id_tenant': ID_TENANT,
                     'username': 'user',
                     'password': '123ABCa.',
                     'first_name': 'Predrag',
                     'last_name': 'Trajkovic',
                     'monthly_income': 20000
                 })

        self.assertEqual(200, self.last_code)
        self.id_session = self.last_result['id_session']

        self.api(None, 'POST', '/api/users/register',
                 body={
                     'id_tenant': ID_TENANT,
                     'username': 'milos',
                     'password': '123ABCa.',
                     'first_name': 'Milos',
                     'last_name': 'Copic',
                     'monthly_income': 10000
                 })

        self.id_session_milos = self.last_result['id_session']

    def test_add_tr(self):

        self.api(self.id_session, 'POST', '/api/transactions',
                 body={
                     'ttype': 'income',
                     'amount': 10,
                     'description': 'test'
                     })

        print(self.last_code)
        print(self.last_result)

    def test_add_more_transactions_to_user_and_get_them(self):

        self.api(self.id_session, 'POST', '/api/transactions',
                 body={
                     'ttype': 'income',
                     'amount': 200,
                     'description': 'platica'
                 })
        id_transaction=self.last_result['id']
        print(id_transaction)
        self.assertIn('id',self.last_result)

        self.api(self.id_session, 'POST', '/api/transactions',
                 body={
                     'ttype': 'income',
                     'amount': 20,
                     'description': 'bonus'
                 })
        self.api(self.id_session, 'POST', '/api/transactions',
                 body={
                     'ttype': 'outcome',
                     'amount': 70,
                     'description': 'Zenina Torba'
                 })

        self.assertIn('id', self.last_result)

        self.api(self.id_session,'GET','/api/transactions')
        print(self.last_result)
        print(self.last_code)




if __name__ == '__main__':
    unittest.main()


