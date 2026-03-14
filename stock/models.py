from django.db import models

class MedicineMaster(models.Model):
    medicine_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.medicine_name} ({self.brand})"


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    mid = models.OneToOneField(MedicineMaster, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.mid.medicine_name} - {self.quantity}"