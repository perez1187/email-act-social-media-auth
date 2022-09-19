from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . serializers import IncomeSerializer
from .models import Income
from .permissions import IsOwner
from rest_framework import permissions

class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    # we overwrite create
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # we overwrite queryset, list of expenses create by the User
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Income.objects.all()
    lookup_field = "id"

    # we overwrite create ( he deleteid this, because he doesnt need it?)
    # def perform_create(self, serializer):
    #     return serializer.save(owner=self.request.user)

    # we overwrite queryset, list of expenses create by the User
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)