from tests.helper import test_base
import users_api as api
import unittest

import users_api.user_regiter

id_tenant = '00000000-1111-2222-3333-000000000001'
DEFAULT_PASSWORD = "DefaultComplexPassword1._?"


class test_is_valid_username(unittest.TestCase):

    def test_valid_username(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera'))

    def test_invalid_username(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera+zika'))

    def test_invalid_username_invalid_email(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera@zika'))

    def test_invalid_username_invalid_email2(self):
        self.assertFalse(users_api.user_regiter.is_valid_username('pera@zika@mika.com'))

    def test_invalid_username_valid_email(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera@zika.com'))

    def test_invalid_username_valid_email_2(self):
        self.assertTrue(users_api.user_regiter.is_valid_username('pera@zika.co.rs'))


class test_password_strength(unittest.TestCase):
    def test(self):
        # self.assertEqual(5, users_api.user_regiter.password_strength('Pera#.123!_'))
        print(users_api.user_regiter.password_strength(''))


class test_is_valid_password(unittest.TestCase):

    def test_valid_strong_password(self):
        self.assertEqual((True, ''), users_api.user_regiter.is_valid_password('Pera#.123!_'))

    def test_invalid_non_strong_password(self):
        self.assertEqual((False, 'minimum 6 characters is required'), users_api.user_regiter.is_valid_password('pera'))

    def test_invalid_non_strong_password_min_1_uppercase(self):
        self.assertEqual((False, 'minimum 1 uppercase letter is required'), users_api.user_regiter.is_valid_password('peraperic'))

    def test_invalid_non_strong_password_min_1_lowercase(self):
        self.assertEqual((False, 'minimum 1 lowercase letter is required'), users_api.user_regiter.is_valid_password('PERAPERIC'))

    def test_minimum_1_character_is_required(self):
        self.assertEqual((False, 'minimum 1 character is required'), users_api.user_regiter.is_valid_password('123456'))

    def test_minimum_1_number_is_required(self):
        self.assertEqual((False, 'minimum 1 number is required'), users_api.user_regiter.is_valid_password('ABCdefg'))

    def test_password_contains_username(self):
        self.assertEqual((False, 'password should not contains username'), users_api.user_regiter.is_valid_password('Igor123._', 'Igor'))

    def test_minimum_1_spec_char_is_required(self):
        self.assertEqual((False, 'minimum 1 special character !@#$%^&*()_-+=/.,; is required'), users_api.user_regiter.is_valid_password('ABCdefg1'))


class test_register_user(test_base):

    def test_register(self):
        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD))
        self.assertIsNotNone(res)
        self.assertIn('id_user', res)
        self.assertIn('status', res)
        self.assertEqual('ok', res['status'])

    def test_try_register_user_with_existing_username_on_same_tenant(self):
        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD))
        self.assertIsNotNone(res)
        self.assertIn('status', res)
        self.assertIn('id_user', res)
        self.assertEqual('ok', res['status'])

        res = self.a(api.register(id_tenant, 'user', DEFAULT_PASSWORD))
        self.assertNotIn('id', res)
        self.assertIn('id_error', res)
        self.assertIn('status', res)
        self.assertEqual('error', res['status'])
        self.assertEqual('REGISTER_ERROR', res['id_error'])

    def test_try_to_register_user_with_invalid_username(self):
        res = self.a(api.register(id_tenant, 'pera+zika', DEFAULT_PASSWORD))
        self.assertEqual({'status': 'error', 'message': 'invalid username', 'id_error': 'REGISTER_ERROR'}, res)

        res = self.a(api.register(id_tenant, 'p', DEFAULT_PASSWORD))
        self.assertEqual({'status': 'error', 'id_error': 'REGISTER_ERROR', 'message': 'invalid username'}, res)

    def test_try_to_register_user_with_simple_password(self):
        res = self.a(api.register(id_tenant, 'user', 'user123'))
        self.assertIn('id_error', res)
        self.assertEqual('PASSWORD_TO_WEAK', res['id_error'])

class test_login_user(test_base):

    def test_login_user_who_dont_exists(self):

        res = self.a(api.login(id_tenant, 'pera',DEFAULT_PASSWORD))
        self.assertEqual('ERROR_LOGGING_USER', res['id_error'])

    def test_login_user(self):

        res = self.a(api.register(id_tenant, 'zika',DEFAULT_PASSWORD))
        self.assertEqual('ok', res['status'])

        res = self.a(api.login(id_tenant, 'zika',DEFAULT_PASSWORD))
        self.assertEqual('ok', res['status'])
        self.assertIn('id_user', res)
        self.assertIn('id_session', res)
        self.assertIn('expires_on', res)

        id_session = res['id_session']

        res = self.a(api.check(id_session))
        print(res)


class test_user_group(test_base):

    def test_create_group_add_user(self):
        #self.flush_db_at_the_end = False
        res = self.a(api.register(id_tenant, 'Slobz', DEFAULT_PASSWORD))
        self.assertIsNotNone(res)
        self.assertIn('id_user', res)
        self.assertIn('status', res)
        id_user=res['id_user']
        self.assertEqual('ok', res['status'])
        res2=self.a(api.grupe.add("Neka Grupa"))
        self.assertIsNotNone(res2)
        self.assertIn('id', res2)
        id_group=res2['id']
        res3=self.a(api.grupe.get(id_group))

        self.assertIn('id',res3)
        self.assertEqual('Neka Grupa',res3['name'])



        res4=self.a(api.user_regiter.patch_user_group(id_user,id_group))
        print(id_user)
        print(id_group)
        print(res4)


        #self.assertEqual("User dodat u grupu",res4['message'])





