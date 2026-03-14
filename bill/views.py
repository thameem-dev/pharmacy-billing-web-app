from django.shortcuts import render,redirect
from stock import models
from .models import BillMaster,BillDetails
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
import json
from django.http import JsonResponse
from stock import models
from django.contrib import messages

# Create your views here.
@login_required
def billEntry(request):
    if request.method=="POST":
        data = json.loads(request.body.decode("utf-8"))
        amount = data.get('amount')
        gst = data.get('gst')
        grand_total = data.get('grand_total')
        items = data.get('items')

        bill_master_object = BillMaster.objects.create(amount=amount,gst=gst,grand_total=grand_total,user=request.user)

        for item in items:
            mid = models.MedicineMaster.objects.get(id=item.get('mid'))
            stock = models.Stock.objects.get(mid=mid)
            stock.quantity = stock.quantity - item.get('qty')
            stock.save()
            BillDetails.objects.create(bill_no=bill_master_object,mid=mid,quantity=item.get('qty'),unit_price=item.get('price'),amount=item.get('total'))
            
        messages.success(request,'Bill saved')
        return JsonResponse({
        "status": "ok",
        "redirect_url": "/bill/billentry/"
    })

    stock = models.Stock.objects.all()
    last_record = BillMaster.objects.last()

    if last_record:
        billno = last_record.id + 1
    else:
        billno = 1

    now = datetime.now()
    return render(request,'billentry.html',{'stock':stock,'bill_no':billno,'bill_date':now})

@login_required
def SalesReport(request):
    data_list = []

    if request.method == "POST":
        f_date_str = request.POST.get('from_date')
        t_date_str = request.POST.get('to_date')

        # Convert string to Python date
        f_date = datetime.strptime(f_date_str, "%Y-%m-%d").date()
        t_date = datetime.strptime(t_date_str, "%Y-%m-%d").date()

        # If bill_date is a DateTimeField, use __date
        data_list = BillMaster.objects.filter(bill_date__date__gte=f_date, bill_date__date__lte=t_date)
        print(data_list)
        # If bill_date is a DateField, you can just use:
        # data_list = BillMaster.objects.filter(bill_date__gte=f_date, bill_date__lte=t_date)

    return render(request, 'sales_report.html', {'datas': data_list})

