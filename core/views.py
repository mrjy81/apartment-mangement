from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .form import CalendarForm, ExpensesPriceForm, CreateMonthlyExpensesForm
from jdatetime import datetime, date
from .models import MonthlyExpense, FlatFeesPerMonth, Flat, ExpensesPrice


def get_current_month_expenses(year, month, day):
    if year and month and day:
        try:
            year = int(year)
            month = int(month)
            day = int(day)

        except ValueError:
            raise Http404("Invalid date")
        monthly_expenses = MonthlyExpense.objects.all()
        for me in monthly_expenses:
            if me.for_date.year == year and me.for_date.month == month:
                return me


def get_today():
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    return year, month, day


def index(request):
    form = CalendarForm()
    year, month, day = get_today()
    if request.method == 'POST':
        date_value = request.POST.get('date')
        try:
            year, month, day = date_value.split('/')
        except Exception as e:
            print(e)
            raise Http404('went wrong')
        return redirect('expense', year=year, month=month, day=day)

    context = {
        'year': year,
        'month': month,
        'day': day,
        'form': form}
    return render(request, 'index.html', context=context)


def expenses(request, year=None, month=None, day=None):
    context = {'date': date(int(year), int(month), int(day))}
    this_month_expense = get_current_month_expenses(year, month, day)
    if this_month_expense:
        flat_fees = FlatFeesPerMonth.objects.filter(monthly_expenses=this_month_expense)
        if flat_fees:
            common_expenses = this_month_expense.expenses.filter(expense__individually=False)
            individual_expenses = this_month_expense.expenses.filter(expense__individually=True)

            context['common_expenses'] = [{"name": ce.expense.name, "price": ce.price} for ce in common_expenses]
            context['individual_expenses'] = [{"name": ie.expense.name, "price": ie.price} for ie in
                                              individual_expenses]

            context['flat_fees'] = flat_fees
            context['apartment_population'] = flat_fees.first().flat.apartment.total_population
            context['total_flats'] = Flat.objects.count()
            context['all_expenses'] = this_month_expense.sum_of_expenses
            context['all_received'] = flat_fees.filter(is_paid=True).count() * flat_fees.first().money.price

    return render(request, 'expense.html', context=context)


def change_monthly_expenses(request, year=None, month=None, day=None):
    context = {}
    this_month_expense = get_current_month_expenses(year, month, day)
    monthly_expenses = MonthlyExpense.objects.all()
    for me in monthly_expenses:
        if me.for_date.year == year and me.for_date.month == month:
            this_month_expense = me
            break
    if this_month_expense:
        expense_prices = this_month_expense.expenses.all()
        if request.method == 'POST':
            all_prices = request.POST.getlist('price')
            price_dict = {expense_price.id: price for expense_price, price in zip(expense_prices, all_prices)}

            for expense_price in expense_prices:
                if expense_price.id in price_dict:
                    expense_price.price = price_dict[expense_price.id]
                    expense_price.save()
            return redirect('expense', year, month, day)

        # Create a form for each expense price
        forms = [ExpensesPriceForm(instance=expense_price) for expense_price in expense_prices]

        context['forms'] = forms
        context['month'] = month
        context['year'] = year
    return render(request, "edit_expense_price.html", context=context)


def edit_paid_expenses(request, flat_per_month_pk):
    if request.method == 'POST':
        flat_per_month = FlatFeesPerMonth.objects.get(pk=flat_per_month_pk)
        year = flat_per_month.monthly_expenses.for_date.year
        month = flat_per_month.monthly_expenses.for_date.month
        day = flat_per_month.monthly_expenses.for_date.day
        is_paid = request.POST.get('is_paid')
        if is_paid == "yes":
            flat_per_month.is_paid = False
        elif is_paid == "no":
            flat_per_month.is_paid = True
        flat_per_month.save()
        return JsonResponse({'year': year, 'month': month, 'day': day})


def create_monthly_expense(request, year=None, month=None, day=None):
    me_form = CreateMonthlyExpensesForm()
    form = ExpensesPriceForm()

    context = {'me_form': me_form, 'form': form}
    return render(request, 'create_monthly_expenses.html', context=context)
