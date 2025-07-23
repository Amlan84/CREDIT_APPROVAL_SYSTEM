from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta, date
from django.http import JsonResponse
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
import math

def home(request):
    return JsonResponse({"message": "Credit Approval System Backend is Running!"})

class RegisterCustomer(APIView):
    def post(self, request):
        data = request.data
        salary = data.get('monthly_income')
        approved_limit = round((36 * salary) / 100000) * 100000

        customer = Customer.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            monthly_income=salary,
            approved_limit=approved_limit,
            phone_number=data.get('phone_number')
        )
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CreateLoan(APIView):
    def post(self, request):
        data = request.data
        customer_id = data.get('customer_id')

        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=404)

        loan_amount = float(data.get('loan_amount'))
        interest_rate = float(data.get('interest_rate'))
        tenure = int(data.get('tenure'))

        r = interest_rate / (12 * 100)
        emi = (loan_amount * r * math.pow(1 + r, tenure)) / (math.pow(1 + r, tenure) - 1)

        end_date = date.today() + timedelta(days=tenure * 30)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_installment=emi,
            end_date=end_date,
            emis_paid_on_time=0,
            repayments_left=tenure
        )

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
