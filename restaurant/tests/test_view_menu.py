from django.test import TestCase, Client
from django.urls import reverse
from ..models import MenuItem, Category

class MenuViewTestCase(TestCase):
    def setUp(self):
        # Create a sample Category instance for testing
        self.category = Category.objects.create(
            slug="sample-category",
            title="Sample Category",
        )

        # Create a sample MenuItem instance for testing
        self.menu_item = MenuItem.objects.create(
            title="Sample Item",
            price=10.99,
            featured=True,
            description="A delicious sample item",
            category=self.category,
        )

    def test_menu_view(self):
        # Create a test client
        client = Client()

        # Simulate a request to the 'menu' view
        response = client.get(reverse('menu'))

        # Check if the response uses the correct template
        self.assertTemplateUsed(response, 'menu.html')

        # Check if the menu data is present in the context
        self.assertIn('menu', response.context)
        menu_data = response.context['menu']
        self.assertTrue(menu_data)  # Assuming you're using QuerySet

        # Clean up (delete the sample menu item if created)
        self.menu_item.delete()
