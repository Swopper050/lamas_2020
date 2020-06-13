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
import types
import os
from server import Agents, simulation

def home(request):
	context = {
	"form":InputForms
	}
	return render(request, 'index.html',context)

def load_inputs(request):

	form = InputForms(request.POST)
	if form.is_valid():
		ui_input = types.SimpleNamespace(
			ndays=form.cleaned_data['number_of_days'],
			nbuyers=form.cleaned_data['number_of_buyers'],
			nsellers=form.cleaned_data['number_of_sellers'],
			lowprice=form.cleaned_data['min_price'],
			highprice=form.cleaned_data['max_price']
		)
		if os.path.exists("./static/plots/simulation_fig.png"):
			os.remove("./static/plots/simulation_fig.png")
		av_transaction_prices, av_seller_prices, av_buyer_prices = simulation.simulation(ui_input)

	return render(request, 'results.html', {"avg_transaction":av_transaction_prices,"avg_seller":av_seller_prices,"avg_buyer":av_buyer_prices})
