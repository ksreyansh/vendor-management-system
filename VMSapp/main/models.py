from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class VendorModel(models.Model):
    vendor_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50)
    contact_details = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    on_time_delivery_rate = models.FloatField(blank=True)
    quality_rating_avg = models.FloatField(blank=True)
    average_response_time = models.FloatField(blank=True)
    fulfillment_rate = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.vendor_code})"

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"


class PurchaseOrderModel(models.Model):
    STATUS_CHOICES = (('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled'))

    po_number = models.CharField(max_length=10, primary_key=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    delivery_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True)
    quality_rating = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0), \
                                                                          MaxValueValidator(5.0)])
    issue_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    acknowledgement_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    completion_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"Order ID: {self.po_number} for (Vendor: {self.vendor.vendor_code})"

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0), \
                                                                              MaxValueValidator(5.0)])
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Historical Performance"
        verbose_name_plural = "Historical Performance"
