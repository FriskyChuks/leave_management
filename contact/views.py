from email import message
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *


def contact_address_views(request,id):
	user = User.objects.get(id=id)
	check_contact = Contact.objects.filter(user_id=user.id)
	contact_form = ContactForm()
	address_form =AddressForm()
	if request.method == 'POST':
		if check_contact:
			messages.error(request,'Your Contact information had previously been captured')
			return redirect('staff_biodata',id=id)
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

def load_state(request):
	state_id = request.GET.get('state_id')
	lgas = LocalGovernmentArea.objects.filter(state=state_id)
	return render(request,'contacts/state_list.html',{"lgas":lgas})

def edit_contact_address_views(request,id):
	user = User.objects.get(id=id)
	contact = Contact.objects.get(user=user)
	address = Address.objects.get(user=user)
	update_contact_form = UpdateContactForm(instance=contact)
	update_address = UpdateAddressForm(instance=address)
	if request.method == 'POST':
		update_contact_form = UpdateContactForm(request.POST,request.FILES, instance=contact)
		update_address = UpdateAddressForm(request.POST,request.FILES, instance=address)
		if update_contact_form.is_valid() and update_address.is_valid():
			update_contact_form.save(commit=False)
			update_address.save(commit=False)
			update_contact_form.user_id = id
			update_address.user_id = id
			update_contact_form.save()
			update_address.save()
			return redirect('staff_biodata',id=id)
	context = {'user':user,'contact':contact,'address':address,
				'form':update_contact_form,'update_address':update_address}
	return render(request,'contacts/edit_contact_address.html',context)

