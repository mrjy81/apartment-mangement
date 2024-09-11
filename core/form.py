from django_jalali.forms import forms
from django_jalali.forms import forms as jalaliforms
from .models import ExpensesPrice, MonthlyExpense, Expense

from core.models import Expense


class CalendarForm(forms.Form):
    calendar = jalaliforms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class ExpensesPriceForm(forms.ModelForm):
    class Meta:
        model = ExpensesPrice
        fields = ['price', ]


class CreateMonthlyExpensesForm(forms.ModelForm):
    class Meta:
        model = MonthlyExpense
        fields = ['expenses', 'for_date', 'description']
        widgets = {
            'expenses': forms.SelectMultiple(attrs={'class': 'custom-multiselect'}),
        }
