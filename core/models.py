from django.db import models
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    name = models.CharField(max_length=100)
    individually = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ExpensesPrice(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    for_date = jmodels.jDateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.expense.name + str(self.price)


class MonthlyExpense(models.Model):
    expenses = models.ManyToManyField(ExpensesPrice, blank=True)
    for_date = jmodels.jDateField()
    description = models.TextField(blank=True, null=True)
    sum_of_expenses = models.PositiveIntegerField(null=True, blank=True, default=0)
    month_finished = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" % (self.for_date, self.sum_of_expenses)


class Flat(models.Model):
    users = models.ManyToManyField(User)
    population = models.IntegerField(default=4)
    name = models.CharField(max_length=100)
    apartment = models.ForeignKey('Apartment', on_delete=models.DO_NOTHING, default='عباس زاده')

    def __str__(self):
        return self.name


class Money(models.Model):
    price = models.PositiveIntegerField(default=0, )
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.price


class FlatFeesPerMonth(models.Model):
    flat = models.ForeignKey('Flat', on_delete=models.DO_NOTHING)
    total_fees = models.PositiveIntegerField(default=0)
    monthly_expenses = models.ForeignKey(MonthlyExpense, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    money = models.ForeignKey(Money, on_delete=models.DO_NOTHING, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If money is not set, try to get the default Money instance
        if not self.money:
            try:
                default_money = Money.objects.get(is_default=True)
                self.money = default_money
            except Money.DoesNotExist:
                # Handle case where no default Money instance exists
                self.money = None  # Or handle as needed

        super(FlatFeesPerMonth, self).save(*args, **kwargs)

    def __str__(self):
        return "%s --> %s" % (self.flat.name, self.total_fees)


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    total_population = models.IntegerField(default=0)

    def __str__(self):
        return self.name


@receiver(post_save, sender=MonthlyExpense)
def update_flat_fees_on_expense_change(sender, instance, created, **kwargs):
    count_of_flats = Flat.objects.count()
    for flat in Flat.objects.all():
        flat_fees, is_flat = FlatFeesPerMonth.objects.get_or_create(
            monthly_expenses=instance,
            flat=flat,
        )
        common_expenses = instance.expenses.filter(expense__individually=False)
        individual_expenses = instance.expenses.filter(expense__individually=True)
        total = (sum(ce.price for ce in common_expenses) / count_of_flats) + (
                (sum(ie.price for ie in individual_expenses) / flat.apartment.total_population) * flat.population)
        flat_fees.total_fees = total
        flat_fees.save()


@receiver(post_save, sender=Flat)
def update_apartment_population(sender, instance, created, **kwargs):
    if not created:
        total = 0
        for f in Flat.objects.all():
            total += f.population

        apartment = Apartment.objects.get(name=instance.apartment.name)
        apartment.total_population = total
        apartment.save()


@receiver(post_save, sender=Money)
def update_default_money(sender, instance, created, **kwargs):
    if not created and instance.is_default:
        Money.objects.exclude(pk=instance.pk).update(is_default=False)


@receiver(post_save, sender=MonthlyExpense)
def update_sum_of_prices(sender, instance, created, **kwargs):
    if not created:
        sum_all = sum(expense.price for expense in instance.expenses.all())
        if sum_all != instance.sum_of_expenses:  # Check if the sum has changed
            instance.sum_of_expenses = sum_all
            instance.save(update_fields=['sum_of_expenses'])  # Only update the sum_of_expenses field


@receiver(post_save, sender=ExpensesPrice)
def update_default_money(sender, instance, created, **kwargs):
    if not created:
        MonthlyExpense.objects.get(expenses=instance).save(update_fields=['sum_of_expenses'])
