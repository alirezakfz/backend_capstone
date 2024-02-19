from django.test import TestCase
from ..models import MenuItem, Category

class MenuItemModelTestCase(TestCase):
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

    def test_menu_item_str(self):
        # Test the __str__ method
        expected_str = "Sample Item : 10.99"
        self.assertEqual(str(self.menu_item), expected_str)

    def test_menu_item_defaults(self):
        # Test default values
        self.assertTrue(self.menu_item.featured)

    def test_menu_item_category(self):
        # Test the category field
        self.assertEqual(self.menu_item.category, self.category)
