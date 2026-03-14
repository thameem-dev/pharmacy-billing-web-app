from django.db import models
from stock.models import MedicineMaster
from django.conf import settings
from django.utils import timezone
# Create your models here.
class BillMaster(models.Model):
    bill_date = models.DateTimeField(default = timezone.now())
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bill {self.id} - {self.user.username}"
    

class BillDetails(models.Model):
    bill_no = models.ForeignKey(BillMaster, on_delete=models.CASCADE)
    mid = models.ForeignKey(MedicineMaster, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bill_no.id} - {self.mid.medicine_name}"