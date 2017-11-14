from django.shortcuts import render
from Online_Financial_Management_System.decorators import custom_login_required
from Online_Financial_Management_System.utils import get_slice_and_page_end, redirect_with_data
from accounts.models import Staff
from companies.models import Company
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from errors.views import error_404 as custom_error_404
from salary.models import Salary


@custom_login_required
def salary(request, data, **kwargs):
    payer = Staff.objects.get(user=request.user)
    owned_companies = Company.objects.filter(owner=payer)

    # Conditions on two kinds of url.
    if 'company_uuid' not in kwargs and 'page_num' not in kwargs:
        # No parameters

        # Test whether the staff has companies.
        if not owned_companies:
            data['no_owned_company'] = True
            return render(request, 'salary/index.html', data)

        first_company_uuid = owned_companies[0].unique_id
        return redirect_with_data(request, data, '/salary/' + str(first_company_uuid) + '/1/')
    else:
        # Two parameters
        data['no_owned_company'] = False
        data['owned_companies'] = owned_companies

        company_uuid = kwargs['company_uuid']
        page_num = kwargs['page_num']
        page_num = int(page_num)

        # If page number is zero...
        if page_num == 0:
            return custom_error_404(request, data)

        # If company_uuid is invalid...
        try:
            company = Company.objects.get(unique_id=company_uuid)
        except ValidationError:
            return custom_error_404(request, data)
        except ObjectDoesNotExist:
            return custom_error_404(request, data)

        # If the logged staff is not the owner of the company:
        if company.owner != payer:
            return custom_error_404(request, data)

        # Get UUID.
        data['company_uuid'] = company.unique_id

        # Get all salary belonging to staffs in the company.
        salary_records = Salary.objects.filter(company=company)

        # If there is no salary record in company...
        if not salary_records:
            data['no_salary_records'] = True
        else:
            data['no_salary_records'] = False

            # Get sliced records.
            data['salary_records'], data['page_end'] = get_slice_and_page_end(salary_records, page_num)

            # Get other necessary data.
            data['page_range'] = range(1, data['page_end'] + 1)
            data['page_num'] = page_num

            # If sliced records are empty...
            if not data['salary_records']:
                return custom_error_404(request, data)

        return render(request, 'salary/index.html', data)


@custom_login_required
def details(request, data, salary_id):
    # If salary_id is invalid...
    try:
        salary_record = Salary.objects.get(id=salary_id)
    except ValidationError:
        return custom_error_404(request, data)
    except ObjectDoesNotExist:
        return custom_error_404(request, data)

    data['salary'] = salary_record
    return render(request, 'salary/details.html', data)


@custom_login_required
def delete(request, data):
    if request.method == 'POST':
        # Collect form data.
        salary_id = request.POST['salary_id']

        # Get Salary instance.
        salary_record = Salary.objects.get(id=salary_id)

        # Delete
        salary_record.delete()

        # Success
        data['alerts'].append(('success', 'Delete successfully!', 'You have successfully deleted a record of salary.'))
        return redirect_with_data(request, data, '/salary/')
    else:
        return custom_error_404(request, data)


@custom_login_required
def create(request, data, **kwargs):
    if request.method == 'POST':
        # Collect form data.
        company_uuid = request.POST['company_uuid']
        payee_id = request.POST['payee_id']
        base_salary = request.POST['base_salary']
        bonus = request.POST['bonus']
        total = request.POST['total']
        date = request.POST['date']

        # Create new salary instance.
        payee = Staff.objects.get(id=payee_id)
        payer = Staff.objects.get(user=request.user)
        company = Company.objects.get(unique_id=company_uuid)
        new_salary = Salary(payer=payer, payee=payee, company=company, base_salary=base_salary, bonus=bonus,
                            total=total, date=date)
        new_salary.save()

        # Success
        data['alerts'].append(('success', 'Create successfully!', 'You have successfully create a new salary record.'))
        return redirect_with_data(request, data, '/salary/')
    else:
        payer = Staff.objects.get(user=request.user)
        company_uuid = kwargs['company_uuid']

        # If company_uuid is invalid...
        try:
            company = Company.objects.get(unique_id=company_uuid)
        except ValidationError:
            return custom_error_404(request, data)
        except ObjectDoesNotExist:
            return custom_error_404(request, data)

        # If the logged staff is not the owner of the company:
        if company.owner != payer:
            return custom_error_404(request, data)

        # Get UUID.
        data['company_uuid'] = company.unique_id

        # Get all staff in this company.
        data['company_staff'] = company.staff.all()

        return render(request, 'salary/create.html', data)
