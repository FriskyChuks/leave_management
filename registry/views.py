from django.shortcuts import render,redirect

from accounts.models import *

from .models import *
from .forms import *


def employment_detail_view(request,id):
    user = User.objects.get(id=id)
    grades = GradeLevel.objects.all()
    salary = SalaryScale.objects.all()
    if request.method == 'POST':
        ministry = request.POST['ministry']
        designation = request.POST['designation']
        salary_scale = request.POST['salary_scale']
        grade = request.POST['grade']
        step = request.POST['step']
        ippis_no = request.POST['ippis_no']
        if int(grade) < 6:
            staff_category_id = 1
        else:
            staff_category_id = 2

        details= EmploymentDetails( user_id=id,ministry=ministry,designation=designation,
                                    salary_scale_id=salary_scale, grade_id=grade, step=step,
                                    ippis_no=ippis_no, staff_category_id=staff_category_id
                                )
        details.save();

        return redirect('contact_address',id=id) 
    context = { 'user':user, 'salary':salary,"grades":grades}
    return render(request, 'registry/employ.html',context) 


def edit_employment_detail_view(request,id):
    employmentdetail = EmploymentDetails.objects.get(id=id)
    user = employmentdetail.user
    form = edit_Employment_DetailsForm(instance=employmentdetail)

    if request.method == 'POST':
        form = edit_Employment_DetailsForm(request.POST,request.FILES, instance=employmentdetail)
        if form.is_valid():
            form.save(commit=False)
            form.user_id = id
            form.save()
            return redirect('edit_contact_address',id=user.id)
    context =  {'form': form, 'user':user}
    return render(request, 'registry/edit_employment_detail.html',context)  


    
                                                  