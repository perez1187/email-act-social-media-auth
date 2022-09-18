from django.urls import path
from . import views

# expenses/
urlpatterns = [
    path('', views.ExpenseListAPIView.as_view(), name="expenses"),
    path('<int:id>', views.ExpenseDetailAPIView.as_view(), name="expense"),
]