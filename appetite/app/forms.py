from django import forms
from .models import register, delivery_agent, supplier_surplus_food, surplus_food_supplier, complaints, feedbacks


class registerform(forms.ModelForm):
    address=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    forms.Textarea(attrs={'rows': 2, 'cols': 15}),
    class Meta():
         model= register
         fields=('name','address','phone_no','state','district','city','email','profile_pic','id')

class Edituserform(forms.ModelForm):
    class Meta():
        address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,}))
        model= register
        fields=('profile_pic','name','address','phone_no','state','district','city','password',)

class Loginform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    class Meta():
        model = register
        fields = ('email','password')

class supplierregform(forms.ModelForm):
    CHOICES = [
        ('Restaurant', 'Restaurant'),
        ('Event Management', 'Event Management'),
    ]
    supplier_type= forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
        model = surplus_food_supplier
        fields = ('supplier_type','name', 'address', 'phone_no', 'state', 'district', 'city', 'email', 'password', 'profile_pic',
        'id')


class Editsupplierregform(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
        model = surplus_food_supplier
        fields = ('profile_pic','name', 'address', 'phone_no', 'state', 'district', 'city', 'password', )

class addDeliveryAgentForm(forms.ModelForm):
    class Meta():
        model = delivery_agent
        fields = ('name','email','profile_pic','id_proof')


class Editadminprofileform(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,}))
    class Meta():
        model= register
        fields=('name','address','phone_no','password',)



class Addsurplusform(forms.ModelForm):

    details=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= supplier_surplus_food
         fields=('details','image')

class editsurplusform(forms.ModelForm):
    details=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= supplier_surplus_food
         fields=('image','details',)


class createComplaintForm(forms.ModelForm):
    complaint = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, }))
    class Meta():
        model = complaints
        fields = ('complaint',)

class replyComplaintForm(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, }))
    class Meta():
        model = complaints
        fields = ('reply',)

class givefeedbackForm(forms.ModelForm):
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, }))
    class Meta():
        model = feedbacks
        fields = ('feedback',)

class replyfeedbackForm(forms.ModelForm):
    reply = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, }))
    class Meta():
        model = feedbacks
        fields = ('reply',)

