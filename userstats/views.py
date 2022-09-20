from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from rest_framework import response, status

'''
    endpoint view for some calcs from db
    https://www.youtube.com/watch?v=x2tDVfl4dg4&list=PLx-q4INfd95EsUuON1TIcjnFZSqUfMf7s&index=16

'''

class ExpenseSummaryStats(APIView):

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0

        for expense in expenses:
            amount +=expense.amount
        return{'amount': str(amount)}

    def get_category(self, expense):
        return expense.category

    def get(self,request):
        todays_date = datetime.date.today
        ayear_ago= todays_date - datetime.timedelta(days=365)
        expensens = Expense.objects.filter(owner=request.user, date__gte=ayear_ago, date__lte=todays_date)

        final = {}
        categories = list(set(map(self.get_categoy, expensens))) # set -> we dont have duplicated

        for expense in expensens:
            for category in categories:
                final[category]= self.get_amount_for_category(expensens, category)

        return response.Response({'category_data':final}, status=status.HTTP_200_OK)