from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Set, Profile
from payment.models import ShippingAddress

class StoreViewsTestCase(TestCase):
    def setUp(self):
        """Set up non-modified objects used by all test methods."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='test@example.com')
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.set = Set.objects.create(name='Test Set', slug='test-set')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            set=self.set,
            price=10.00
        )
        Profile.objects.get_or_create(user=self.user)

    def test_home_view(self):
        """Test the home page view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('products', response.context)

    def test_about_view(self):
        """Test the about page view."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_product_view_success(self):
        """Test the product detail view with an existing product."""
        response = self.client.get(reverse('product', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product.html')
        self.assertEqual(response.context['product'], self.product)

    def test_product_view_not_found(self):
        """Test the product detail view with a non-existent product."""
        response = self.client.get(reverse('product', args=['non-existent-slug']))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_category_view_success(self):
        """Test the category view with an existing category."""
        response = self.client.get(reverse('category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertEqual(response.context['searchCategory'], self.category)
        self.assertQuerySetEqual(response.context['products'], [self.product])

    def test_set_view_success(self):
        """Test the set view with an existing set."""
        response = self.client.get(reverse('set', args=[self.set.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertEqual(response.context['searchCategory'], self.set)
        self.assertQuerySetEqual(response.context['products'], [self.product])

    def test_register_user_view(self):
        """Test user registration."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout_user_view(self):
        """Test user login and logout."""
        # Test login
        self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword123'})
        response = self.client.get(reverse('update_user'))
        self.assertEqual(response.status_code, 200)

        # Test logout
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('update_user'))
        self.assertEqual(response.status_code, 302)

    def test_update_user_view_authenticated(self):
        """Test update user view when logged in."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('update_user'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser_updated@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertContains(response, 'Profile updated successfully!')

    def test_update_password_view(self):
        """Test password update view."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('update_password'), {
            'old_password': 'testpassword123',
            'new_password1': 'new_password_456',
            'new_password2': 'new_password_456',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(self.client.login(username='testuser', password='testpassword123'))

    def test_update_info_view(self):
        """Test update info view for profile and shipping."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('update_info'), {
            'phone': '1234567890',
            'shipping_full_name': 'Test User',
            'shipping_email': 'shipping@example.com',
            'shipping_address1': '123 Test St',
            'shipping_city': 'Testville',
            'shipping_state': 'TS',
            'shipping_zipcode': '12345',
            'shipping_country': 'Testland',
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.phone, '1234567890')

    def test_search_view(self):
        """Test the search functionality."""
        response = self.client.post(reverse('search'), {'search_query': 'Test Product'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertQuerySetEqual(response.context['products'], [self.product])
