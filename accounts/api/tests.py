from accounts.models import UserProfile
from rest_framework.test import APIClient
from testing.testcases import TestCase

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

class AccountApiTests(TestCase):
    
    def setUp(self):
        # run at very test function
        self.client = APIClient()
        self.user = self.create_user(
            username='admin',
            email='admin@hotmail.com',
            password='correct password',
        )
    

    def test_login(self):
        # every test function needs to start with test_ to be used
        # test must use post, not get
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # log in failed, http status code return 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # use post but with wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # check not login yet
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # use correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'admin@hotmail.com')

        # check already login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # log in first and tesst
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })

        # check user already logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # test must use post
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # change to post, logout successfully
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        # check if user already logged out
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
    
    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@hotmail.com',
            'password': 'any password',
        }

        # check get request fail
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # check wrong email address
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password'
        })
        #print(response.status_code)
        self.assertEqual(response.status_code, 400)

        # check password too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@hotmail.com',
            'password': '123'
        })
        #print(response.data)
        self.assertEqual(response.status_code, 400)

        # check username too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is toooooo loooooooong',
            'email': 'someone@hotmail.com',
            'password': 'any password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # signup successful
        response = self.client.post(SIGNUP_URL, data)             
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        
        # check user profile has been created
        created_user_id = response.data['user']['id']
        profile = UserProfile.objects.filter(user_id=created_user_id).first()
        self.assertNotEqual(profile, None)

        # check user logged out
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
# Create your tests here.
