from django.test import TestCase
from webapp.models import MyUser, Medicine, PharmacyDepartment, Order, MedSupplier, Promocode, BasketItem, PickUpPoint, Faq, News, MonthPlot, Employee, Vacancy, Review
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from django.template.response import TemplateResponse
import os

class MedicineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        dep1 = PharmacyDepartment.objects.create(all_sold_num = 0, type_of_medicine="med1", description = "med1 description")
        dep1.save()
        med1 = Medicine.objects.create(department = dep1, name="med1")
        med1.save()
        new1 = News.objects.create(news_message = "Message!!!")
        new1.save()
        Faq.objects.create(phone_number="+375296989862", email="jbvbd@mail.com", description="des", adress="adrs")

    def test_index_url(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_dep_url(self):
        request = HttpRequest()
        
        med1 = Medicine.objects.all()
        dep1 = PharmacyDepartment.objects.get()

        # Передаем данные контекста в TemplateResponse
        response = TemplateResponse(request, "department.html", {"meds": med1, "dep": dep1})
        
        # Проверяем статус ответа и тип ответа
        self.assertEqual(response.status_code, 200)
        
        self.assertIsInstance(response, TemplateResponse)

    def test_faq(self):
        resp = self.client.get('/faq/')

        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get('/login/')

        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get('/registration/')

        self.assertEqual(resp.status_code, 200)
         
    def test_rev(self):
        resp = self.client.get('/reviews/')

        self.assertEqual(resp.status_code, 200)

    def test_con(self):
        resp = self.client.get('/faq/contacts/')

        self.assertEqual(resp.status_code, 200)

class MedicineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dep1 = PharmacyDepartment.objects.create(all_sold_num = 0, type_of_medicine="med1", description = "med1 description")
        cls.dep1.save()
        cls.med1 = Medicine.objects.create(department = cls.dep1, name="med1")
        cls.med1.save()

        cls.user = User.objects.create(username="qwertrtfry", first_name="Bob", last_name="Bobsky", email="qwerty@mail.com", password="12345678", is_staff=True, is_superuser=True)
        cls.user.save()
        cls.myuser = MyUser.objects.create(user = cls.user, phone_number = "+375296989862", user_age = 19)
        cls.myuser.save()

        cls.bas_it = BasketItem.objects.create(medicine = cls.med1)

        cls.myuser.basket.add(cls.bas_it)

    def test_account(self):
        self.client.cookies["username"] = self.user.username
        
        response = self.client.get('/account/')

        self.assertEqual(response.status_code, 200)

    def test_account(self):
        self.client.cookies["username"] = self.user.username
        
        response = self.client.get('/account/orders/')

        self.assertEqual(response.status_code, 200)

    def test_account_changeinfo(self):
        self.client.cookies["username"] = self.user.username
        
        response = self.client.get('/account/changeinfo/')

        self.assertEqual(response.status_code, 200)

    def test_account_basket(self):
        self.client.cookies["username"] = self.user.username
        
        response = self.client.get('/basket/')

        self.assertEqual(response.status_code, 200)

    def test_account_basket_order(self):
        self.client.cookies["username"] = self.user.username
        
        response = self.client.get('/basket/order/')

        self.assertEqual(response.status_code, 200)

    def test_graph(self):
        self.client.cookies["username"] = self.user.username
        self.client.cookies["role"] = True
        
        response = self.client.get('/graph/')

        self.assertEqual(response.status_code, 200)

    def test_suppliers(self):
        self.client.cookies["username"] = self.user.username
        self.client.cookies["role"] = True
        
        response = self.client.get('/suppliers/')

        self.assertEqual(response.status_code, 200)