from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test the public available recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test the authirized user ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            '123456'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieve list of recipe"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that recipes returned are for the authenticate user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            '123456'
        )

        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    # def test_create_ingredient_successful(self):
    #     """Test creating a new ingredients"""
    #     payload = {'name': 'Cabbage'}
    #     self.client.post(RECIPES_URL, payload)
    #
    #     exists = Recipe.objects.filter(
    #         user=self.user,
    #         name=payload['name']
    #     ).exists()
    #     self.assertTrue(exists)
    #
    # def test_create_tag_invalid(self):
    #     """Test creating a new ingredients with invalid payload"""
    #     payload = {'name': ''}
    #     res = self.client.post(RECIPES_URL, payload)
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
