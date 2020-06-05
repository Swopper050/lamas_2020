from django import forms

int_choices= [tuple([x,x]) for x in range(1,10)]
class InputForms(forms.Form):
    number_of_days = forms.IntegerField(label="Days for Simulation", widget=forms.Select(choices=int_choices))
    number_of_buyers = forms.IntegerField(label="Number of Buyers", widget=forms.Select(choices=int_choices))
    number_of_sellers = forms.IntegerField(label="Number of Sellers", widget=forms.Select(choices=int_choices))
