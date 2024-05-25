from django.contrib import admin
from .models import MyUser, Medicine, PharmacyDepartment, Order, MedSupplier, Promocode, BasketItem, PickUpPoint, Faq, News, MonthPlot, Employee, Vacancy, Review

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Medicine)
admin.site.register(PharmacyDepartment)
admin.site.register(Order)
admin.site.register(MedSupplier)
admin.site.register(Promocode)
admin.site.register(BasketItem)
admin.site.register(PickUpPoint)
admin.site.register(Faq)
admin.site.register(News)
admin.site.register(MonthPlot)
admin.site.register(Review)
admin.site.register(Vacancy)
admin.site.register(Employee)