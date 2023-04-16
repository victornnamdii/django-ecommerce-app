from django import forms

from datetime import datetime


class PaymentForm(forms.Form):
    firstname = forms.CharField(max_length=50,
                                min_length=4,
                                error_messages={
                                    'required': 'Please enter a valid name'},
                                label='First Name', widget=forms.TextInput(
                                    attrs={'placeholder': 'First Name',
                                           'id': 'fname',
                                           'name': 'fname'}
                                ), required=True)
    lastname = forms.CharField(max_length=50,
                               min_length=4,
                               error_messages={
                                'required': 'Please enter a valid name'},
                               label='Last Name', widget=forms.TextInput(
                                    attrs={'placeholder': 'Last Name'}
                                ), required=True)
    email = forms.EmailField(max_length=100,
                             error_messages={
                                'required': 'Please enter a valid email'},
                             widget=forms.TextInput(
                                attrs={'placeholder': 'johndoe@example.com'}
                             ), required=True)
    address1 = forms.CharField(max_length=250, label='Address Line 1',
                               widget=forms.TextInput(
                                attrs={'placeholder': '542 W. 15th Street'}
                               ), required=True)
    address2 = forms.CharField(max_length=250, label='Address Line 2',
                               widget=forms.TextInput(
                                attrs={'placeholder': 'Optional'}
                               ), required=False)
    city = forms.CharField(max_length=20,
                           widget=forms.TextInput(
                                attrs={'placeholder': 'City'}
                               ), required=True)
    state = forms.CharField(max_length=20, required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'State'}
                            ))
    zipcode = forms.CharField(max_length=20, required=True,
                              widget=forms.TextInput(
                                attrs={'placeholder': '10001'}
                                ))
    phone_number = forms.CharField(max_length=20, required=True,
                                   widget=forms.TextInput(
                                    attrs={'placeholder': '08101234567'}
                                    ))
    name_on_card = forms.CharField(max_length=100, required=True,
                                   widget=forms.TextInput(
                                    attrs={'placeholder': 'John Doe'}
                                    ))
    cardno = forms.CharField(min_length=14, max_length=19, label='Card Number',
                             required=True)
    expirymonth = forms.IntegerField(max_value=12, min_value=1,
                                     label='Expiry month', required=True)
    expiryyear = forms.IntegerField(min_value=datetime.now().year,
                                    label='Expiry year', required=True)
    cvv = forms.CharField(max_length=3, required=True,
                          label='CVV')

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(cvv) != 3:
            raise forms.ValidationError('Enter complete CVV')
        return cvv
