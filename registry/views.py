from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd

from accounts.models import *
from contact.models import Contact

from .models import *
from .forms import *


def employment_detail_view(request, id):
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
        if len(ippis_no) != 0:
            if len(ippis_no) < 6 or len(ippis_no) > 6:
                messages.error(request, 'IPPIS-NO must be 6-digits!')
                return redirect('employment_detail', id=id)
        if int(grade) < 6 and salary_scale == 1:
            staff_category_id = 1
        else:
            staff_category_id = 2

        details = EmploymentDetails(user_id=id, ministry=ministry, designation=designation,
                                    salary_scale_id=salary_scale, grade_id=grade, step=step,
                                    ippis_no=ippis_no, staff_category_id=staff_category_id
                                    )
        details.save()

        return redirect('contact_address', id=id)
    context = {'user': user, 'salary': salary, "grades": grades}
    return render(request, 'registry/employ.html', context)


def edit_employment_detail_view(request, id):
    employmentdetail = EmploymentDetails.objects.get(id=id)
    user = employmentdetail.user
    form = edit_Employment_DetailsForm(instance=employmentdetail)

    if request.method == 'POST':
        form = edit_Employment_DetailsForm(
            request.POST, request.FILES, instance=employmentdetail)
        if form.is_valid():
            form.save(commit=False)
            form.user_id = id
            form.grade_id = employmentdetail.grade
            form.save()
            try:
                Contact.objects.get(user_id=user.id)
                return redirect('edit_contact_address', id=user.id)
            except ObjectDoesNotExist:
                return redirect('contact_address', id=user.id)
    context = {'form': form, 'user': user,
               'employmentdetail': employmentdetail}
    return render(request, 'registry/edit_employment_detail.html', context)


# def update_db_by_excel_file(request):
#     employment_detail_dict = {}
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         if file.name.endswith('.xlsx'):
#             df = pd.read_excel(file)
#             # collect data and append to dictionary
#             for _, row in df.iterrows():
#                 if not pd.isna(row['FILE NO.']):
#                     # {'key':{'key':'value'}}
#                     email = row['E-MAIL']
#                     dob = row['DATE OF BIRTH'],
#                     employment_detail_dict[int(row['FILE NO.'])] = {
#                         'qualifications': row['QUALIFICATIONS/DATES'],
#                         'rank': row['PRESENT RANK'],
#                         'first_appointment_date': row['DATE OF 1ST APPT'],
#                         'confirmation_date': row['DATE OF CONFIRMATION'],
#                         'date_of_appt_with_fmc': row['DATE OF APPT FMC'],
#                         'present_appt_date': row['DATE OF PRESENT APPT'],
#                     }

#                     try:
#                         user = User.objects.get(
#                             file_number=int(row['FILE NO.']))
#                         # Contact.objects.update_or_create(
#                         #     user_id=user.id, defaults={'email': row['E-MAIL']})
#                         EmploymentDetails.objects.update_or_create(
#                             user_id=user.id, defaults={
#                                 'qualifications': row['QUALIFICATIONS/DATES'],
#                                 'rank': row['PRESENT RANK'],
#                                 'first_appointment_date': row['DATE OF 1ST APPT'],
#                                 'confirmation_date': row['DATE OF CONFIRMATION'],
#                                 'date_of_appt_with_fmc': row['DATE OF APPT FMC'],
#                                 'present_appt_date': row['DATE OF PRESENT APPT'],
#                             })
#                     except:
#                         pass

#             print(employment_detail_dict)
#             return render(request, 'registry/import_excel.html', {'message': 'Updated successfully'})
#         else:
#             return render(request, 'registry/import_excel.html', {'message': 'Invalid file format. Please upload an Excel file (.xlsx).'})

#     return render(request, 'registry/import_excel.html', {'message': 'File uploaded successfully'})
