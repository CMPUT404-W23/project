from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.
class AccountsUITest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Log In')

    def test_signup_page(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
        self.assertContains(response, 'Sign Up')
    
    def test_settings_page(self):
        user = User.objects.create_user(username='testuser', password='django404')
        self.client.force_login(user)
        url = reverse('settings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')
        self.assertContains(response, 'Settings')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'GitHub')
        self.assertContains(response, 'Profile Image Link')
