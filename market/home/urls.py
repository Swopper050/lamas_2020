# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:59:04 2020

@author: 91782
"""
from django.urls import path
from .views import home, load_inputs, introduction, problem_description, model, experiments


urlpatterns = [
    path('', home, name='home'),
    path('home', home, name='home'),
    path('start_sim', load_inputs, name='start_sim'),
    path('introduction', introduction, name='introduction'),
    path('problem_description', problem_description, name='problem_description'),
    path('model', model, name='model'),
    path('experiments', experiments, name='experiments'),
]
