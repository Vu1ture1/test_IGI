from django.test import TestCase
from webapp.models import MyUser, Medicine, PharmacyDepartment, Order, MedSupplier, Promocode, BasketItem, PickUpPoint, Faq, News, MonthPlot, Employee, Vacancy, Review
from django.contrib.auth.models import User
from LabaDjWeb.forms import RegisterForm, ChangeForm

class RegisterFormTest(TestCase):
    def test_register_form_valid(self):
        form_data = {
            'username': 'test_user',
            'password': 'test_password',
            'password_con': 'test_password',
            'email': 'test@example.com',
            'phone_number': '+375291234567',
            'age': 25,
            'f_name': 'Test',
            'l_name': 'User'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid(self):
        form_data = {
            'username': '',
            'password': 'short',
            'password_con': 'password',
            'email': 'invalid_email',
            'phone_number': '123',
            'age': 15,
            'f_name': '',
            'l_name': ''
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        #print(form.errors)


class ChangeFormTest(TestCase):
    def test_change_form_valid(self):
        form_data = {
            'username': 'test_user',
            'email': 'new_email@example.com',
            'phone_number': '+375291234567',
            'age': 30,
            'f_name': 'New',
            'l_name': 'Name'
        }
        form = ChangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_form_invalid(self):
        form_data = {
            'username': 'test_user',
            'email': 'invalid_email',
            'phone_number': '123',
            'age': 15,
            'f_name': '',
            'l_name': ''
        }
        form = ChangeForm(data=form_data)
        self.assertFalse(form.is_valid())
        #print(form.errors)