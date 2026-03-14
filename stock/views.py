from django.shortcuts import render
from django.contrib import messages
from .models import MedicineMaster,Stock
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def addMedicine(request):
    if request.method == "POST":
        medicine_name =  str(request.POST.get('medicine_name'))
        brand = str(request.POST.get('brand'))

        if medicine_name != medicine_name.strip() or brand != brand.strip():
            messages.error(request,"Remove unwanted whitespace")
        else:
            if MedicineMaster.objects.filter(medicine_name__icontains=medicine_name):
                messages.error(request,"Medicine name already exist")
                return render(request,'add_medicine.html')
            if MedicineMaster.objects.filter(medicine_name=medicine_name).exists():
                messages.error(request,"Medicine name already exist")
            else:
                MedicineMaster.objects.create(medicine_name=medicine_name,brand=brand)
                messages.success(request,"Medicine added")
    return render(request,'add_medicine.html')

@login_required
def addStock(request):
    medicines = MedicineMaster.objects.all()
    if request.method == "POST":
        id = request.POST.get('mid')
        brand = request.POST.get('brand')
        quantity = int(request.POST.get('quantity'))
        unit_price = float(request.POST.get('unitprice'))

        print(quantity<0)
        # validation
        if quantity<=0:
            messages.error(request,"Invalid quantity")
            return render(request,'add_stock.html',{'medicines':medicines})
        
        if unit_price<=0:
            messages.error(request,"Invalid unit price")
            return render(request,'add_stock.html',{'medicines':medicines})

        medicine_obj = MedicineMaster.objects.get(id=id)
        try :
            stock_obj = Stock.objects.get(mid=medicine_obj)
            stock_obj.quantity = quantity
            stock_obj.unit_price = unit_price
            stock_obj.save()
            messages.success(request,'Stock updated')
        except Exception as e:
            Stock.objects.create(mid=medicine_obj,unit_price=unit_price,quantity=quantity)
            messages.success(request,'Stock added')
        
    medicines = MedicineMaster.objects.all()
    return render(request,'add_stock.html',{'medicines':medicines})

@login_required
def stocksList(request):
    stock = Stock.objects.all()
    return render(request,'stocks_list.html' , {'stock':stock})