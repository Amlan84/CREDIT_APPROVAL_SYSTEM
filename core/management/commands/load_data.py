import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer, Loan

class Command(BaseCommand):
    help = 'Load customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        self.load_customers()
        self.load_loans()

    def load_customers(self):
        df = pd.read_excel('customer_data.xlsx')
        for _, row in df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'phone_number': row['Phone Number'],
                    'monthly_income': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit']
                }
            )
        self.stdout.write(self.style.SUCCESS('✅ Customers loaded successfully.'))

    def load_loans(self):
        df = pd.read_excel('loan_data.xlsx')
        for _, row in df.iterrows():
            customer = Customer.objects.filter(customer_id=row['Customer ID']).first()
            if customer:
                Loan.objects.update_or_create(
                    loan_id=row['Loan ID'],
                    defaults={
                        'customer': customer,
                        'loan_amount': row['Loan Amount'],
                        'interest_rate': row['Interest Rate'],
                        'tenure': row['Tenure'],
                        'monthly_payment': row['Monthly payment'],
                        'emis_paid_on_time': row['EMIs paid on Time'],
                        'start_date': row['Date of Approval'],
                        'end_date': row['End Date']
                    }
                )
        self.stdout.write(self.style.SUCCESS('✅ Loans loaded successfully.'))
