# tests/test_my_protected_controller.py

from odoo.tests.common import HttpCase

class TestMyProtectedController(HttpCase):

    def setUp(self):
        super(TestMyProtectedController, self).setUp()
        # Create a test user with appropriate permissions
        self.user = self.env.ref('base.user_demo')  # Reference a test user
        # Ensure the test user is activated
        # self.env.user = self.user

    def test_my_protected_page_authenticated(self):
        self.env.user = self.user
        # Simulate HTTP request with an authenticated user
        with self.url_open('/supplier/view') as response:
            self.assertEqual(response.status_code, 200)
            print(response.__dict__)
            # self.assertIn(b'House', response)

    def test_my_protected_page_unauthenticated_redirect(self):
        # Simulate HTTP request without authentication
        with self.url_open('/supplier/view', headers={'X-Openerp-Session-Id': ''}) as response:
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'/web/login', response.headers.get('Location', b''))
