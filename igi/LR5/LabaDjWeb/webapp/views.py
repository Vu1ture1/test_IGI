from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import MyUser, Medicine, PharmacyDepartment, Order, MedSupplier, BasketItem, PickUpPoint, Faq, News, MonthPlot,Review, Employee, Vacancy
from LabaDjWeb.forms import RegisterForm, LoginForm, ChangeForm
from django.contrib.auth.models import User
import django.shortcuts
import requests
#from cyrtranslit import to_latin
from googletrans import Translator
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import operator
import threading
from datetime import datetime
import logging
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(level=logging.INFO, filename="D:\django\LabaDjWeb\webapp\py_log.log", filemode="a+", format="%(asctime)s %(levelname)s %(message)s")

def index(request):
    deps = PharmacyDepartment.objects.all()

    try:
        news = News.objects.latest('date_created')
    except ObjectDoesNotExist:
        news = "0"

    logging.info("view index")

    return TemplateResponse(request, "index.html", context={"deps": deps, "news": news})
    
def faq(request):
    vacs = Vacancy.objects.all()

    faq = Faq.objects.all()

    logging.info("view faq")

    return TemplateResponse(request, "faq.html", {"info": faq, "vacs": vacs})

def registration(request):
    if(request.method == "POST"):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            phone_num = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            age = form.cleaned_data["age"]
            username = form.cleaned_data["username"]
            f_name = form.cleaned_data["f_name"]
            l_name = form.cleaned_data["l_name"]

            user = User.objects.create_user(email=email, password=password, username=username, first_name = f_name, last_name = l_name)

            MyUser.objects.create(user=user, phone_number = phone_num, user_age = age)

            logging.info("registration complited")

            return django.shortcuts.redirect('/login')
        else:
            logging.error("registration failed")
            return TemplateResponse(request, "registration.html", {"form":form, "errors":form.errors.values()})
        
    return TemplateResponse(request, "registration.html", {"form": RegisterForm})

def login(request):
    if(request.method == "POST"):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]

            user = User.objects.get(username = username)

            response = django.shortcuts.redirect('/')
            response.set_cookie('username', username, max_age=3600) # Куки на 1 час
            if user.is_superuser == True:
                response.set_cookie('role', True, max_age=3600) # Куки на 1 час
            else:
                response.set_cookie('role', user.is_staff, max_age=3600) # Куки на 1 час

            response.set_cookie('admin', user.is_superuser, max_age=3600) # Куки на 1 час

            logging.info("sign in complited")

            return response
        else:
            logging.error("sign in error")
            return TemplateResponse(request, "login.html", {"form": form, "errors": form.errors.values()})
        
    return TemplateResponse(request, "login.html", {"form": LoginForm})

def logout(request):
    if request.COOKIES.get("username") != None:
        response = django.shortcuts.redirect('/')

        response.delete_cookie("username")
        response.delete_cookie("role")

        logging.info("log out complited")

        return response
    else:
        return django.shortcuts.redirect('/')
    
def department(request):
    if(request.method == "GET"):
        logging.info("view department")
        
        id = request.GET.get("id")

        prev = request.META.get("HTTP_REFERER")

        if request.GET.get("med_id") != None:
            id = request.GET.get("id")
            med = Medicine.objects.get(id = request.GET.get("med_id"))
            user = User.objects.get(username = request.COOKIES["username"])

            myuser = MyUser.objects.get(user = user)

            if myuser.basket.filter(medicine=med).exists():
                bi = myuser.basket.get(medicine=med)
                
                bi.quantity += 1

                bi.save() 
            else:
                new_bi = BasketItem(medicine = med)

                new_bi.save()

                myuser.basket.add(new_bi)

            return django.shortcuts.redirect(prev)

        if request.GET.get("order") == "price_low":
            dep = PharmacyDepartment.objects.get(id = id)

            meds = Medicine.objects.filter(department = dep).order_by("-price")

            return TemplateResponse(request, "department.html", {"meds": meds, "dep": dep})
        elif request.GET.get("order") == "price_high":
            dep = PharmacyDepartment.objects.get(id = id)

            meds = Medicine.objects.filter(department = dep).order_by("price")

            return TemplateResponse(request, "department.html", {"meds": meds, "dep": dep})
        else:
            dep = PharmacyDepartment.objects.get(id = id)

            meds = Medicine.objects.filter(department = dep)

            return TemplateResponse(request, "department.html", {"meds": meds, "dep": dep})
    else: 
        return django.shortcuts.redirect('/')

def basket(request):
    if request.COOKIES.get("username") != None:
        
        logging.info("view basket")
        
        prev = request.META.get("HTTP_REFERER")
        
        user = User.objects.get(username = request.COOKIES["username"])

        myuser = MyUser.objects.get(user = user)

        if request.GET.get("basket_item_id") != None:
            id = request.GET.get("basket_item_id")

            basketItem = BasketItem.objects.get(id = id)

            if basketItem.quantity == 1:
                myuser.basket.remove(basketItem)
                basketItem.delete() 
            else:
                basketItem.quantity -= 1
                basketItem.save()

            return django.shortcuts.redirect(prev)

        if request.GET.get("order") == "price_low":
            basket_list = list(myuser.basket.all().order_by('medicine__name'))
        elif request.GET.get("order") == "price_high":
            basket_list = list(myuser.basket.all().order_by('-medicine__name'))
        else: 
            basket_list = list(myuser.basket.all())

        num = 0.0

        for el in basket_list:
            num += el.quantity * el.medicine.price
        
        return TemplateResponse(request, "basket.html", {"basket": basket_list, "total": round(num, 3)})
    
    else:
        return django.shortcuts.redirect('/')

def order(request):
    if request.COOKIES.get("username") != None:
        
        user = User.objects.get(username = request.COOKIES["username"])

        myuser = MyUser.objects.select_related('user').prefetch_related('basket', 'my_promocodes', 'my_orders').get(user=user)

        basket_list = list(myuser.basket.all())

        num = 0.0

        for el in basket_list:
            num += el.quantity * el.medicine.price

        if request.POST.get("my_option") != None:
            discount = float((request.POST.get("my_option")).replace(',', '.'))

            if discount != 0:
                promo = myuser.my_promocodes.get(discount = discount)
                myuser.my_promocodes.remove(promo)
                myuser.save()

            point = PickUpPoint.objects.get(id = int(request.POST.get("my_option_point")))

            num -= discount

            if num < 0:
                num = 0
            else:
                order = Order.objects.create(user=user, total_price=num)
                order.meds.set(myuser.basket.all())
                order.pick_up_point = point

                for el in myuser.basket.all():
                    el.medicine.all_sold_num += el.quantity

                    el.medicine.save()

                    el.medicine.department.all_sold_num += el.medicine.price * el.quantity

                    el.medicine.department.save()
                    
                order.save()
                myuser.basket.clear()
                myuser.save()

                return django.shortcuts.redirect('/')

        logging.info("create order")

        return TemplateResponse(request, "order.html", {"total": num, "list": list(myuser.my_promocodes.all()), "points": list(PickUpPoint.objects.all())})
    
    else:
        return django.shortcuts.redirect('/')

def internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def account(request):
    if request.COOKIES.get("username") != None:
        
        user = User.objects.get(username = request.COOKIES["username"])

        myuser = MyUser.objects.select_related('user').prefetch_related('basket', 'my_promocodes', 'my_orders').get(user=user)

        if internet_connection() == True:
            logging.info("internet connection is here")
            translator = Translator()
                
            name = translator.translate(user.first_name, dest="en").text

            response = requests.get(f'https://api.nationalize.io/?name={name}')
            response1 = requests.get(f'https://api.genderize.io/?name={name}')
        
            data = response.json()
            data1 = response1.json()

            if data['country']:
                country_ids = [country['country_id'] for country in data['country']]
                probability = ', '.join(country_ids) + '.'
            else:
                probability = "Не определен"

            if data1['gender']:
                gender = translator.translate(data1['gender'], dest="ru").text
            else:
                gender = "Не определен"
        else:
            logging.error("no internet connection")
            probability = "Не определен, нет подключения к интернету"
            gender = "Не определен, нет подключения к интернету"
        
        user_timezone = timezone.get_current_timezone()

        logging.info("view account")

        return TemplateResponse(request, "account.html", {"user": myuser, "json": probability, "nameAPI": gender, "time_zone": user_timezone})
    
    else:
        return django.shortcuts.redirect('/')
    
def orders(request):
    if request.COOKIES.get("username") != None:
        
        user = User.objects.get(username = request.COOKIES["username"])

        myorders = Order.objects.prefetch_related('meds').filter(user=user).order_by('-date_created')

        logging.info(f"view orders")

        return TemplateResponse(request, "orders.html", {"myorders": myorders})
    
    else:
        return django.shortcuts.redirect('/')
    
def changeinfo(request):
    if(request.method == "POST"):
        form = ChangeForm(request.POST)
        
        if form.is_valid():
            phone_num = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            age = form.cleaned_data["age"]
            username = form.cleaned_data["username"]
            f_name = form.cleaned_data["f_name"]
            l_name = form.cleaned_data["l_name"]

            user = User.objects.get(username = request.COOKIES["username"])

            myuser = MyUser.objects.select_related('user').prefetch_related('basket', 'my_promocodes', 'my_orders').get(user=user)

            if phone_num != "+37529":
                myuser.phone_number = phone_num
            
            if email != "":
                user.email = email

            if age != None:
                myuser.user_age = age
            
            if username != "":
                user.username = username

            if f_name != "":
                user.first_name = f_name

            if l_name != "":
                user.last_name = l_name
            
            user.save()

            myuser.save()

            response = django.shortcuts.redirect('/account')
                
            response.delete_cookie("username")
            response.set_cookie('username', user.username, max_age=3600)
            response.delete_cookie("role")
            response.set_cookie('role', user.is_staff, max_age=3600) 

            logging.info("change account information")

            return response
        else:
            logging.error("change account information error")
            return TemplateResponse(request, "changeinfo.html", {"form":form, "errors":form.errors.values()})
        
    return TemplateResponse(request, "changeinfo.html", {"form": ChangeForm})

def suppliers(request):
    if request.COOKIES.get("username") != None:
        
        user = User.objects.get(username = request.COOKIES["username"])

        if user.is_staff == True or user.is_superuser == True:
            supp = MedSupplier.objects.all()
            logging.info("view suppliers info")
            return TemplateResponse(request, "suppliers.html", {"supply": supp})
        else:
            return django.shortcuts.redirect('/')

    return django.shortcuts.redirect('/')

def generate_plot_and_save():
    timem = datetime.today()
    orders = Order.objects.filter(date_created__month=timem.month)
    date_price_pairs = [(order.date_created.day, order.total_price) for order in orders]
    sorted_date_price_pairs = sorted(date_price_pairs, key=operator.itemgetter(0))
    dates, values = zip(*sorted_date_price_pairs)

    plt.plot(dates, values, marker='o', linestyle='-', color='red')
    plt.xlabel('Дата в днях')
    plt.ylabel('Цены заказов руб.')
    plt.title('График по всем заказам в течении месяца')

    plt.savefig('D:\\django\\LabaDjWeb\\media\\images\\plot.png')
    plt.close()

def graph(request):
    if request.COOKIES.get("username") != None:
        
        user = User.objects.get(username=request.COOKIES["username"])

        if user.is_staff or user.is_superuser:
            logging.info("create graph in other stream")
            
            plot_thread = threading.Thread(target=generate_plot_and_save)
            
            plot_thread.start()
            
            plot_thread.join()

            logging.info("graph created")

            MonthPlot.objects.all().delete()

            new_obj = MonthPlot.objects.create()

            timem = datetime.today()

            orders = Order.objects.filter(date_created__month=timem.month)

            values = [order.total_price for order in orders]

            total = round(sum(values), 2)

            logging.info("view graph")
            
            return TemplateResponse(request, "graph.html", {"graph_path": new_obj, "total": total})

        else:
            return django.shortcuts.redirect('/')
    
    return django.shortcuts.redirect('/')

def review(request):
    if(request.method == "POST"):
        user = User.objects.get(username = request.COOKIES["username"])

        con = request.POST.get("text")

        stars = request.POST.get("ran")

        rev = Review.objects.create(user = user, context = con, mark = stars)

        rev.save()

        logging.info("creating review")

        return django.shortcuts.redirect('/reviews')

    coms = Review.objects.order_by('-id')[:20]
    
    return TemplateResponse(request, "review.html", {"comments": coms})

def contacts(request):
    emp = Employee.objects.all()

    logging.info("view contacts")

    return TemplateResponse(request, "contacts.html", {"emp": emp})

def news(request):
    news = News.objects.order_by('-date_created')

    logging.info("view news")

    return TemplateResponse(request, "news.html", context={"news": news})