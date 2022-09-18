from rest_framework import serializers
from .models import Expense

class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = fields = ['date', 'description', 'amount', 'category']

    