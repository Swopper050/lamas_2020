from django import forms

MARKET_SITUATIONS = [
    ("negotiation", "Negotiation"),
    ("grocery_store", "Grocery Store"),
]

class InputForms(forms.Form):
    market_situation = forms.ChoiceField(label="Market Situation", choices=MARKET_SITUATIONS)
    number_of_days = forms.IntegerField(label="Days for Simulation", initial=3000)
    number_of_buyers = forms.IntegerField(label="Number of Buyers", initial=100)
    number_of_sellers = forms.IntegerField(label="Number of Sellers", initial=100)
    min_price = forms.IntegerField(label="Minimum Price", initial=1)
    max_price = forms.IntegerField(label="Maximum Price", initial=20)
