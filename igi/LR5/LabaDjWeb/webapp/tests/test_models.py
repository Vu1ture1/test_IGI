from django.test import TestCase
from webapp.models import MyUser, Medicine, PharmacyDepartment, Order, MedSupplier, Promocode, BasketItem, PickUpPoint, Faq, News, MonthPlot, Employee, Vacancy, Review
from django.contrib.auth.models import User
import os

class MyUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="qwerty", first_name="Bob", last_name="Bobsky", email="qwerty@mail.com", password="12345678")
        MyUser.objects.create(user = user, phone_number = "+375296989862", user_age = 19)

    def test_phone_number_label(self):
        myuser = MyUser.objects.get(id=1)
        ph_label = myuser._meta.get_field("phone_number").verbose_name
        self.assertEquals(ph_label, 'phone number')

    def test_phone_number_max_lenght(self):
        myuser = MyUser.objects.get(id=1)
        ph_len = myuser._meta.get_field("phone_number").max_length
        self.assertEquals(ph_len, 13)

    def test_age_num(self):
        myuser = MyUser.objects.get(id=1)
        age = myuser._meta.get_field("user_age").verbose_name
        self.assertEquals(age, 'user age')


class MedicineModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Medicine.objects.create(name="1234")

    def test_default_code_label(self):
        med = Medicine.objects.get(id=1)
        c_label = med._meta.get_field("code").default
        self.assertEquals(med.code, c_label)

    def test_code_label(self):
        med = Medicine.objects.get(id=1)
        c_label = med._meta.get_field("code").verbose_name
        self.assertEquals(c_label, 'code')

    def test_code_max_lenght(self):
        med = Medicine.objects.get(id=1)
        c_len = med._meta.get_field("code").max_length
        self.assertEquals(c_len, 20)

    def test_name_max_lenght(self):
        med = Medicine.objects.get(id=1)
        name_len = med._meta.get_field("name").max_length
        self.assertEquals(name_len, 125)

    def test_default_instruction_label(self):
        med = Medicine.objects.get(id=1)
        i_label = med._meta.get_field("instruction").default
        self.assertEquals(med.instruction, i_label)

    def test_instruction_label(self):
        med = Medicine.objects.get(id=1)
        i_label = med._meta.get_field("instruction").verbose_name
        self.assertEquals(i_label, 'instruction')

    def test_instruction_max_lenght(self):
        med = Medicine.objects.get(id=1)
        i_len = med._meta.get_field("instruction").max_length
        self.assertEquals(i_len, 1000)

    def test_default_description_label(self):
        med = Medicine.objects.get(id=1)
        d_label = med._meta.get_field("description").default
        self.assertEquals(med.description, d_label)

    def test_description_label(self):
        med = Medicine.objects.get(id=1)
        d_label = med._meta.get_field("description").verbose_name
        self.assertEquals(d_label, 'description')

    def test_description_max_lenght(self):
        med = Medicine.objects.get(id=1)
        d_len = med._meta.get_field("description").max_length
        self.assertEquals(d_len, 1000)


    def test_default_price_num(self):
        med = Medicine.objects.get(id=1)
        p_num = med._meta.get_field("price").default
        self.assertEquals(med.price, p_num)

    def test_price_label(self):
        med = Medicine.objects.get(id=1)
        p_label = med._meta.get_field("price").verbose_name
        self.assertEquals(p_label, 'price')

    def test_image_field_contains_image(self):
        med = Medicine.objects.get(id=1)
        image_path = med.med_png.path
        self.assertTrue(os.path.exists(image_path), f"Image file '{image_path}' does not exist")
    

    

    

