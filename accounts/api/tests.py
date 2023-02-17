from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

class AccountApiTests(TestCase):
    """
    this is a unit test class
    use it to generate test data function
    """

    def setUp(self):
        # be called at every test function executed
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@hotmail.com',
            password='correct password',
        )

    def createUser(self, username, email, password):
        # cannot use User.objects.create()
        # because password has to be crypto, username and email need some normalization
        return User.objects.create_user(username, email, password)
    
    def test_login(self):
        # for unit test, function has to start with test_ can be used to automatic test
        # test needs POST, not GET
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })

        # failed login, http status code return 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # user use post but with wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password'
        })
        self.assertEqual(response.status_code, 400)

        # check not login yet

        # used correct password
        # check already logged in