from django.test import Client, TestCase
from django.urls import reverse

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
