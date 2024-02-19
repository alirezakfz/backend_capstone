from django.test import TestCase
from ..models import Category

class CategoryModelTestCase(TestCase):
    def setUp(self):
        # Create a sample Category instance for testing
        self.category = Category.objects.create(
            slug="sample-category",
            title="Sample Category",
        )

    def test_category_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.category), "Sample Category")

    def test_category_slug(self):
        # Test the slug field
        self.assertEqual(self.category.slug, "sample-category")