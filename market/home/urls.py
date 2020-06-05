# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:59:04 2020

@author: 91782
"""
from django.urls import path
from .views import home, load_inputs


urlpatterns = [
    path('home', home, name = 'home'),
    path('start_sim',load_inputs, name = 'start_sim')
]
