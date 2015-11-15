from django.test import SimpleTestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class ViewsTests(SimpleTestCase):

    def setUp(self):
        self.c = Client()
        self.username = 'z@z.com'
        self.password = '12345'
        self.user = User.objects.create_user('z@z.com', 'z@z.com', '12345')

    def test_dashboard_get(self):
        self.c.post(reverse('login'), {'username': self.username, 'password': self.password})
        response = self.c.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')
