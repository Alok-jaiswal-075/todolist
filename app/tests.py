from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Tag, TODO
from datetime import datetime, timedelta
from django.urls import reverse
from django.test import Client


class ModelTesting(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password'
        )
        self.tag = Tag.objects.create(name='TestTag')
        self.todo = TODO.objects.create(
            title='Test TODO',
            description='Test description',
            due_date=datetime.now() + timedelta(days=1),
            status='OPEN',
            user=self.user
        )
        self.todo.tags.add(self.tag)

    def test_tag_model(self):
        tag = self.tag
        self.assertTrue(isinstance(tag, Tag))
        self.assertEqual(str(tag), 'TestTag')

    def test_todo_model(self):
        todo = self.todo
        self.assertTrue(isinstance(todo, TODO))
        self.assertEqual(str(todo), 'Test TODO')
        self.assertEqual(todo.status, 'OPEN')
        self.assertEqual(todo.user, self.user)
        self.assertTrue(self.tag in todo.tags.all())

    def test_todo_completed_status(self):
        todo = TODO.objects.create(
            title='Test Completed TODO',
            description='Test description for completed todo',
            status='COMPLETED',
            user=self.user
        )
        self.assertEqual(todo.status, 'COMPLETED')

    def test_todo_invalid_status(self):
        with self.assertRaises(ValueError):
            TODO.objects.create(
                title='Test Invalid Status TODO',
                description='Test description for invalid status todo',
                status='INVALID',
                user=self.user
            )

    def test_tag_name_length(self):
        max_length = Tag._meta.get_field('name').max_length
        long_name = 'a' * (max_length + 1)
        with self.assertRaises(Exception):
            Tag.objects.create(name=long_name)

    def test_tag_uniqueness(self):
        with self.assertRaises(Exception):
            Tag.objects.create(name='TestTag')

    def test_todo_without_description(self):
        todo = TODO.objects.create(
            title='Test TODO Without Description',
            status='OPEN',
            user=self.user
        )
        self.assertEqual(todo.description, '')

    def tearDown(self):
        get_user_model().objects.all().delete()
        Tag.objects.all().delete()
        TODO.objects.all().delete()


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password'
        )

    def test_home_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the home page")

    def test_unsuccessful_login(self):
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login failed")

    def test_signup_invalid_data(self):
        response = self.client.post(reverse('signup'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signup failed")

    def test_unauthorized_access(self):
        response = self.client.get(reverse('add_todo'))
        self.assertEqual(response.status_code, 302)

    def test_add_todo_authenticated(self):
        self.client.force_login(self.user)
        todo_data = {'title': 'Test Todo', 'description': 'Test Description'}
        response = self.client.post(reverse('add_todo'), todo_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TODO.objects.count(), 1)

    def test_delete_todo_authenticated(self):
        todo = TODO.objects.create(title='Test Todo', description='Test Description', user=self.user)
        response = self.client.get(reverse('delete_todo', kwargs={'id': todo.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TODO.objects.count(), 0)

    def test_change_todo_authenticated(self):
        todo = TODO.objects.create(title='Test Todo', description='Test Description', user=self.user)
        response = self.client.get(reverse('change_todo', kwargs={'id': todo.id, 'status': 'completed'}))
        self.assertEqual(response.status_code, 200)
        updated_todo = TODO.objects.get(id=todo.id)
        self.assertEqual(updated_todo.status, 'completed')

    def test_all_tasks_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('all_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_specific_task_authenticated(self):
        self.client.force_login(self.user)
        todo = TODO.objects.create(title='Test Todo', description='Test Description', user=self.user)
        response = self.client.get(reverse('specific_task', kwargs={'task_id': todo.id}))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        get_user_model().objects.all().delete()
