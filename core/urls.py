from django.urls import path
from .views import home, RegisterCustomer, CreateLoan

urlpatterns = [
    path('', home),
    path('register', RegisterCustomer.as_view()),
    path('create-loan', CreateLoan.as_view()),
]
