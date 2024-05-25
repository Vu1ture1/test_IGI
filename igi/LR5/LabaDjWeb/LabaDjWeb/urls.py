"""
URL configuration for LabaDjWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from webapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    re_path(r'^faq/contacts', views.contacts),
    re_path(r'^faq', views.faq),
    re_path(r'^account/changeinfo', views.changeinfo),
    re_path(r'^account/orders', views.orders),
    re_path(r'^account', views.account),
    
    re_path(r'^basket/order', views.order),
    re_path(r'^basket', views.basket),

    re_path(r'^news', views.news),
    
    re_path(r'^department', views.department),
    re_path(r'^registration', views.registration),
    re_path(r'^login', views.login),
    re_path(r'^logout', views.logout),
    re_path(r'^suppliers', views.suppliers),
    re_path(r'^graph', views.graph),

    re_path(r'^reviews', views.review),
    
    re_path(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)