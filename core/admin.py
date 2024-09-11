from django.contrib import admin
from .models import Apartment, Expense, Flat, User, ExpensesPrice, MonthlyExpense, FlatFeesPerMonth, Money
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

admin.site.register(FlatFeesPerMonth)
admin.site.register(MonthlyExpense)
admin.site.register(ExpensesPrice)
admin.site.register(Apartment)
admin.site.register(Expense)
admin.site.register(Money)
admin.site.register(Flat)
admin.site.register(User)
