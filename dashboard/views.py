from calendar import month_name
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import *
# Create your views here.
from bill.models import BillMaster
from django.db.models import Sum


@login_required
def dashboard(request):
    context = { }
    if request.user.role=='biller':
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        user = request.user  # current logged-in biller

        today_sales = (
        BillMaster.objects.filter(
            bill_date__date=today,
            user=user
        ).aggregate(total=Sum("amount"))["total"] or 0
        )

        yesterday_sales = (
        BillMaster.objects.filter(
            bill_date__date=yesterday,
            user=user
        ).aggregate(total=Sum("amount"))["total"] or 0
         )

        context = {
        "today_sales": today_sales,
        "yesterday_sales": yesterday_sales,
            }


    if request.user.role == "manager":
        data = {}
    # Get current year
        year = timezone.now().year

        # Loop through 12 months
        for month in range(1, 12 + 1):
            month_label = month_name[month].lower()[:3]   # "jan", "feb", ...

            records = BillMaster.objects.filter(
                bill_date__year=year,
                bill_date__month=month
            )
            total_sales_amount = 0
            for item in records:
                total_sales_amount += item.grand_total
            data[month_label] = total_sales_amount
        labels = list(data.keys())     # ["jan","feb","mar",...]
        values = list(data.values())   # [18000,15000,...]

        billers_bill = BillMaster.objects.filter(user__role="biller",bill_date__year = timezone.now().year)

        billers_sales = {}
        for item in billers_bill:
            username = item.user.username
            billers_sales[username] = billers_sales.get(username, 0) + item.grand_total
        
        biller_labels = list(billers_sales.keys())     # ["jan","feb","mar",...]
        biller_values = list(billers_sales.values())   # [18000,15000,...]
        context = {
                "labels": labels,
                "values": values,
                'biller_labels' : biller_labels ,
                'biller_values' : biller_values ,
        }

    return render(request, "dashboard.html", context)

   