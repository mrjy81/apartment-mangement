from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change/is-paid/<int:flat_per_month_pk>/', views.edit_paid_expenses, name='change-is-paid'),
    re_path(r'^change/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.change_monthly_expenses,
            name='change_price'),
    re_path(r'^expense/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.expenses, name='expense'),
    re_path(r'^create/monthly/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.create_monthly_expense,
            name='create-monthly'),

]
