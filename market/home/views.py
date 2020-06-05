# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 16:26:11 2020

@author: 91782
"""

from django.shortcuts import render, redirect
import pdb
from .forms import InputForms
from django.template import Context, Template
from django.contrib import messages
def home(request):
	context = {
	"form":InputForms
	}
	return render(request, 'index.html',context)

def load_inputs(request):
	#pdb.set_trace()
	form = InputForms(request.POST)
	#pdb.set_trace()
	if form.is_valid():
		msg_str = "Starting Simulation for " + str(form.cleaned_data['number_of_days']) + " days with " + str(form.cleaned_data['number_of_buyers']) + " buyers and " + str(form.cleaned_data['number_of_sellers']) + " sellers"
		messages.add_message(request, messages.SUCCESS, msg_str)

		#return render(request, 'index.html', {'days':form.cleaned_data['number_of_days'], 'buyers':form.cleaned_data['number_of_buyers'], 'sellers': form.cleaned_data['number_of_sellers']})
	return redirect('home')
