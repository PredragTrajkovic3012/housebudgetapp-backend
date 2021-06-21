import unittest
import json
from tests.helper import test_base_tornado

from tornado.httpclient import AsyncHTTPClient

from tests.test_rest import ID_TENANT
import uuid


class TestGrupeRest(test_base_tornado):

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


    def test_add_Grupa(self):

       # self.flush_db_at_the_end=False
        res=self.add_grupa("Grupa1")

        self.assertIn("id",res)

    def test_get_all_grupe(self):
       # self.flush_db_at_the_end=False
        self.api(self.id_session, 'GET', '/api/grupe')
        self.assertEqual([], self.last_result)


        self.api(self.id_session, 'POST', '/api/grupe', body={'name': 'grupa1'})
        print(self.last_result)
        print(self.last_code)

        self.api(self.id_session, 'GET', '/api/grupe')
        print(self.last_result)
        print(self.last_code)

        self.api(self.id_session_milos, 'POST', '/api/grupe', body={'name': 'grupa1'})
        print(self.last_result)
        print(self.last_code)
        self.api(self.id_session_milos, 'POST', '/api/grupe', body={'name': 'grupa1'})
        print(self.last_result)
        print(self.last_code)

        self.api(self.id_session_milos, 'GET', '/api/grupe')
        print(self.last_result)
        print(self.last_code)

        #
      #  id_grupa = self.last_result['id']
       # self.api(None, 'GET', f'/api/grupe/{id_grupa}')
        #print(self.last_result)
        #print(self.last_code)


        # self.add_trosak('Za klopu na praksi', 200, )
        # self.api(None, 'GET', '/api/troskovi')
        # self.assertEqual(1, len(self.last_result))
        #
        # self.add_trosak('Igoru za casove', 200)
        #
        # res = self.api(None, 'GET', '/api/troskovi')
        # print("RES",res)

        #self.assertEqual(2, len(self.last_result))


    def add_grupa(self, name):
        self.api(self.id_session , 'POST', '/api/grupe',
                 body={
                     'name': name,

                     })
        return self.last_result
        #TODO: assert
        # print(self.last_code)
        # print(self.last_result)


if __name__ == '__main__':
    unittest.main()