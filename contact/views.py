from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *


def contact_address_views(request,id):
	user = User.objects.get(id=id)
	contact_form = ContactForm()
	address_form =AddressForm()
	if request.method == 'POST':
		contact_form = ContactForm(request.POST, request.FILES)
		address_form = AddressForm(request.POST,request.FILES)
		if contact_form.is_valid() and address_form.is_valid():
			contact_form_obj = contact_form.save(commit=False)
			address_form_obj = address_form.save(commit=False)
			contact_form_obj.user_id = id
			address_form_obj.user_id = id
			contact_form_obj.save()
			address_form.save()
			return redirect('staff_biodata',id=id)

	context = {'form':contact_form, 'user':user,'address_form':address_form} 
	return render(request,'contacts/address.html',context)



