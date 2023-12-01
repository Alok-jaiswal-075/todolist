from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tag, TODO
from datetime import datetime, timedelta


class ModelTesting(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password'
        )
        # Create a tag for testing
        self.tag = Tag.objects.create(name='TestTag')
        # Create a TODO instance for testing
        self.todo = TODO.objects.create(
            title='Test TODO',
            description='Test description',
            due_date=datetime.now() + timedelta(days=1),  # Set due date one day from now
            status='OPEN',
            user=self.user
        )
        self.todo.tags.add(self.tag)  # Add the created tag to the TODO

    def test_tag_model(self):
        tag = self.tag
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(str(tag), 'TestTag')  # Check the string representation

    def test_todo_model(self):
        todo = self.todo
        self.assertTrue(isinstance(todo, TODO))
        self.assertEqual(str(todo), 'Test TODO')  # Check the string representation
        self.assertEqual(todo.status, 'OPEN')     # Verify the status attribute
        self.assertEqual(todo.user, self.user)    # Verify the associated user
        self.assertTrue(self.tag in todo.tags.all())  # Verify the associated tag
        # Add more assertions for other attributes as needed
