from rest_framework import serializers
from .models import Income

class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ('__all__')
        
        extra_kwargs = {
            "id": {"read_only":True}
        }

    