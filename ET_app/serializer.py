from rest_framework import serializers
from .models import expense, category

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = expense
        fields = '__all__'
        read_only_fields = ["user"] #this field data only add or modify by server, not does work from frontend

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'
        

        
