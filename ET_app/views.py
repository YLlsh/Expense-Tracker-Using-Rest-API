from django.shortcuts import render, redirect
from .models import *
from .serializer import ExpenseSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

from rest_framework.response import Response

from django.db.models import Sum
# from rest_framework_simplejwt.
# Create your views here.

from django.utils.dateparse import parse_date

def sign_up(request):
    if request.method == "POST":
        username  = request.POST.get("username") 
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create(username = username, email=email)
        user.set_password(password)
        user.save()

        return redirect('login')
    return render(request,"index.html")

class ExpenseView(ModelViewSet):
    queryset = expense.objects.all()
    serializer_class = ExpenseSerializer
    # permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        qs = expense.objects.filter(user=self.request.user)

        from_date = self.request.query_params.get("from")
        to_date = self.request.query_params.get("to")

        if from_date:
            qs = qs.filter(created_at__date__gte=parse_date(from_date))

        if to_date:
            qs = qs.filter(created_at__date__lte=parse_date(to_date))

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@api_view(['GET'])
def CountExpense(request):
    expense_obj = expense.objects.filter(user=1).first()

    total = expense.objects.filter(user=1).aggregate(
        sum_of_expense=Sum('amount')
    )

    return Response({
        'user': expense_obj.user.username,
        'total_sum': total['sum_of_expense']
    })



class CategoryView(ModelViewSet):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

