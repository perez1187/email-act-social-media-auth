from rest_framework import serializers
from .models import Expense

class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ('__all__')
        
        extra_kwargs = {
            "id": {"read_only":True}
        }

    