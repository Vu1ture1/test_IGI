from django.db import models
from django.contrib.auth.models import User

class PharmacyDepartment(models.Model):
    
    all_sold_num = models.FloatField(blank=False, default=0)
    type_of_medicine = models.CharField(blank=False, default=None, max_length=300)
    description = models.CharField(blank=False, default="Нет описания", max_length=1000)

class Medicine(models.Model):
    
    code = models.CharField(blank=False, default="Код продукта", max_length=20)
    name = models.CharField(blank=False, default=None, max_length=125)
    instruction = models.CharField(blank=False, default="Нет инструкции", max_length=1000)
    description = models.CharField(blank=False, default="Нет описания", max_length=1000)
    price = models.FloatField(blank=False, default=0)
    med_png = models.ImageField(blank=True, upload_to="media/images/", default="media/images/noimg.png")
    department = models.ForeignKey(PharmacyDepartment, on_delete=models.CASCADE, 
                                   related_name='pharmacy_department', null=True, default=None)
    
    all_sold_num = models.IntegerField(blank=False, default=0)

class BasketItem(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Promocode(models.Model):
    promo_str = models.CharField(max_length=20, blank=False, default="Промокод")

    discount = models.FloatField(blank=False, default=5)

class PickUpPoint(models.Model):
    pick_up_point =  models.CharField(max_length=100, blank=False, default="Точка самовывоза")

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default=None, related_name='orderer', null=True)

    meds = models.ManyToManyField(BasketItem, related_name='order_medicines', blank=True, default=None)

    pick_up_point = models.ForeignKey(PickUpPoint, blank=False, default=None, on_delete=models.CASCADE, related_name='point', null=True)

    total_price = models.FloatField(blank=False, default=None)

    date_created = models.DateTimeField(auto_now_add=True)

class MyUser(models.Model):
    
    user = models.OneToOneField(User, blank=False, default=None, on_delete=models.CASCADE, related_name='profile', null=True)

    phone_number = models.CharField(max_length=13, blank=False, default=None)

    user_age = models.IntegerField(blank=False)

    basket = models.ManyToManyField(BasketItem, related_name='basket_medicines', blank=True, default=None)

    my_promocodes = models.ManyToManyField(Promocode, related_name='user_promocodes', blank=True, default=None)

    my_orders = models.ManyToManyField(Order, related_name='orders', blank=True)

class MedSupplier(models.Model):
    
    name = models.CharField(blank=False, default=None, max_length=125)
    phone_number = models.CharField(max_length=13, blank=False, default=None)
    email = models.CharField(blank=False, default=None, max_length=125)
    adress = models.CharField(blank=False, default=None, max_length=300)
    description = models.CharField(blank=False, default="Нет описания", max_length=300)

class News(models.Model):
    news_png = models.ImageField(blank=True, upload_to="media/images/", default="media/images/noimg.png")
    news_message = models.CharField(blank=False, default="Содержание", max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

class Vacancy(models.Model):
    name = models.CharField(blank=False, default="Вакансия", max_length=300)
    description = models.CharField(blank=False, default="Ее описание", max_length=3000)
    salary = models.FloatField(blank=False, default=0)

class Employee(models.Model):
    f_name = models.CharField(blank=False, default="Имя", max_length=300)
    l_name = models.CharField(blank=False, default="Фамилия", max_length=300)
    phone_number = models.CharField(max_length=13, blank=False, default=None)
    email = models.CharField(blank=False, default=None, max_length=125)
    emp_png = models.ImageField(blank=True, upload_to="media/images/", default="media/images/noimg.png")
    job_title = models.CharField(blank=False, default=None, max_length=125)

class Faq(models.Model):
    
    phone_number = models.CharField(max_length=13, blank=False, default=None)
    email = models.CharField(blank=False, default=None, max_length=125)
    adress = models.CharField(blank=False, default=None, max_length=300)
    description = models.CharField(blank=False, default=None, max_length=1000)
    vacancies = models.ManyToManyField(Vacancy, related_name='company_vacs', blank=True, default=None)

class MonthPlot(models.Model):
    plot_png = models.ImageField(blank=True, upload_to="media/images/", default="D:/django/LabaDjWeb/media/images/plot.png")

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default=None, related_name='rewiew_user', null=True)
    
    context = models.CharField(blank=False, default="Содержание", max_length=1000)
    
    date_created = models.DateTimeField(auto_now_add=True)

    mark = models.IntegerField(blank=False, default=10)