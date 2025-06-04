"""
URL configuration for dorzi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='iloveu'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('findTailor/', views.findTailor, name='findTailor'),
    path('readyMade/', views.readyMade, name='readyMade'),
    path('productDetail/<int:id>/', views.product_details, name='product_details'),
    path('login/', views.login, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='user_signup'),
    path('tailor_signup/', views.tailor_signup, name='tailor_signup'), 
    path('logout/', views.logout, name='logout'),
    path('profile/<int:id>/', views.buyer_dashboard, name='buyer_dashboard'),
    path('updateuser/<int:id>/', views.updateuser, name='updateuser'),
    path('deleteuser/<int:id>/', views.delete_user, name='deleteuser'),
    path('updateTailor/<int:id>/',views.updatetailor,name='updatetailor'),
    path('deleteTailor/<int:id>/',views.deletetailor,name='deletetailor'),
    
    #------------------------------------------
    path('tailorDeshboard/<int:id>/', views.tailor_dashboard, name='tailor_dashboard'),
    path('tailor_login/', views.tailor_login, name='tailor_login'),
    path('tailor_detail/<int:id>/', views.tailor_details, name='tailor_details'),
    
    #-----------------------------------------
    path('createcontact/', views.createcontact, name='createcontact'),
    
    #-----------------------------------------
    
    path('createporder/<int:bid>/', views.createporder, name='createporder'),
    path('deleteporder/<int:id>/',views.deleteporder, name='deleteporder'),
    
    #------------------------------------------
    
    path('createtoder/<int:bid>/<int:tid>/',views.createtorder,name='createtorder'),
    path('deletetorder/<int:id>/',views.deletetorder,name='deletetorder'),
    
    #-------------------------------------------
    
    path('createreviews/<int:bid>/<int:tid>/<int:pid>/',views.createreviews,name='createreviews'),
    path('deletereviews/<int:id>/',views.deletereviews,name='deletereviews'),
    path('updatereviews/<int:id>/',views.updatereviews,name='updatereviews'),
    
    #-------------------------------------------
    
    path('cart/<int:bid>/',views.cart,name='cart'),
    path('add_to_cart/<int:bid>/<int:pid>/',views.add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:bid>/',views.remove_from_cart,name='remove_from_cart'),
    path('remove_from_cart_single/<int:pid>/<int:bid>/', views.remove_from_cart_single, name='remove_from_cart_single'),
    
    #-------------------------------------------
    
    path('createproduct/<int:tid>/',views.createproduct,name='createproduct'),
    path('updateproduct/<int:id>/',views.updateproduct,name='updateproduct'),
    path('deleteproduct/<int:id>/',views.deleteproduct,name='deleteproduct'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
