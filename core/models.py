from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    emis_paid_on_time = models.IntegerField()
    repayments_left = models.IntegerField()

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer.first_name}"
