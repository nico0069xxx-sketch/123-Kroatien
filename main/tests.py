from django.test import TestCase, Client
from django.urls import reverse

class SmokeTest(TestCase):
    """Minimal smoke tests to verify basic functionality."""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_loads(self):
        """Test that home page returns 200 or redirect."""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_admin_page_loads(self):
        """Test that admin login page loads."""
        response = self.client.get('/nik-verwaltung-2026/')
        self.assertIn(response.status_code, [200, 302])
    
    def test_django_check(self):
        """Test that Django system check passes."""
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('check', stdout=out)
        self.assertIn('System check', out.getvalue())
