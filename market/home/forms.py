from django import forms

int_choices = [tuple([x,x]) for x in range(1,10)]
days_choices = [tuple([x,x]) for x in range(1,30)]
class InputForms(forms.Form):
    number_of_days = forms.IntegerField(label="Days for Simulation")
    number_of_buyers = forms.IntegerField(label="Number of Buyers")
    number_of_sellers = forms.IntegerField(label="Number of Sellers")
    min_price = forms.IntegerField(label="Minimum Price")
    max_price = forms.IntegerField(label="Maximum Price")
