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

def conclusion(request):
	return render(request, 'conclusion.html')

def home(request):
	context = {
		"form": InputForms,
	}
	return render(request, 'index.html', context)


def problem_description(request):
	return render(request, 'problem_description.html')


def model(request):
	return render(request, 'model.html')


def experiments(request):
	return render(request, 'experiments.html')


def load_inputs(request):

	form = InputForms(request.POST)
	if form.is_valid():
		sim_config = types.SimpleNamespace(
			market_situation=form.cleaned_data['market_situation'],
			ndays=form.cleaned_data['number_of_days'],
			nbuyers=form.cleaned_data['number_of_buyers'],
			nsellers=form.cleaned_data['number_of_sellers'],
			lowprice=form.cleaned_data['min_price'],
			highprice=form.cleaned_data['max_price'],
			nbuyer_interactions=form.cleaned_data['n_buyer_interactions'],
			nseller_interactions=form.cleaned_data['n_seller_interactions'],
		)

		if os.path.exists("./static/plots/simulation_fig.png"):
			os.remove("./static/plots/simulation_fig.png")
		av_transaction_prices, av_seller_prices, av_buyer_prices = simulation.simulation(sim_config)
		final_tprice = av_transaction_prices[-1]
		final_bprice = av_buyer_prices[-1]
		final_sprice = av_seller_prices[-1]
		av_transaction_prices = sum(av_transaction_prices) / len(av_transaction_prices)
		av_buyer_prices = sum(av_buyer_prices) / len(av_buyer_prices)
		av_seller_prices = sum(av_seller_prices) / len(av_seller_prices)


	return render(request, 'results.html',
			{"avg_transaction":round(av_transaction_prices,3),
			"avg_seller":round(av_seller_prices,3),
			"avg_buyer":round(av_buyer_prices,3),
			"final_trans":round(final_tprice,3),
			"final_buyer": round(final_bprice,3),
			"final_seller": round(final_sprice,3)})
