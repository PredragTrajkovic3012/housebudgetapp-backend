import unittest
import users_models
import users_api as api
from tests.helper import test_base, test_base_tornado

import users_api.transactiontype as transactiontype_api
import users_api.trosak as transactions_api
import users_api.transtactions as transactions_api
import users_api.user_regiter

id_tenant = '00000000-1111-2222-3333-000000000001'


class test_transactiontype_crud(test_base):

    def test_add_transaction_type(self):

        r = self.assertIn('id', self.a(transactiontype_api.add_transactiontype('Trening','trening.svg')))
        r = self.assertIn('id', self.a(transactiontype_api.add_transactiontype('Za jelo', 'hrana.svg')))
        r = self.assertIn('id', self.a(transactiontype_api.add_transactiontype('Dug', 'dug.svg')))
        r = self.a(transactiontype_api.add_transactiontype('Dug', 'dug.svg'))
        id_transaction_type = r['id']
        #print(id_transaction_type)
        r = self.assertIn('image', self.a(transactiontype_api.getImage(id_transaction_type)))
        image=self.a(transactiontype_api.getImage(id_transaction_type))
        #print(image['image'])
        #r=self.assertIn('id',self.a(transactiontype_api.getImage(id_transaction_type)))
        #self.flush_db_at_the_end = False
    def test_add_transaction_type_to_transaction(self):

        #dodavanje transakcionog tipa
        r = self.assertIn('id', self.a(transactiontype_api.add_transactiontype('plata', 'plata.svg')))
        r = self.a(transactiontype_api.add_transactiontype('Plata','kad se plata primi', 'plata.svg'))
        id_transaction_type = r['id']
        #print(id_transaction_type)


        #dodavanje usera i transakcije
        user1 = self.a(users_api.user_regiter.register(id_tenant, "PeraZmaj", "Peraglava123!", "Petar", "Peric", 20000))
        r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 200, 'plata')))
        r = self.assertIn('id', self.a(transactions_api.add_transaction('income', user1['id_user'], 20, 'bonus',id_transaction_type)))
        r = self.assertIn('image', self.a(transactiontype_api.getImage(id_transaction_type)))
        print(self.a(transactiontype_api.getImage(id_transaction_type)))
        self.flush_db_at_the_end = False
        #id_transaction=self.a(transactions_api.add_transaction('income', user1['id_user'], 200, 'plata'))['id']
    def test_add_array_of_ttypes(self):
        r = self.assertIn('status', self.a(transactiontype_api.setTransactionTypes()))
        #print(self.a(transactiontype_api.setTransactionTypes()))
        #print(self.a(transactiontype_api.get_all_transaction_types()))
        self.flush_db_at_the_end = False












if __name__ == '__main__':
    unittest.main()
