from django.contrib import admin

from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel
# Register your models here.


@admin.register(VendorModel)
class VendorModelAdmin(admin.ModelAdmin):
    list_display = ['vendor_code', 'name']
    ordering = ("vendor_code",)


@admin.register(PurchaseOrderModel)
class PurchaseOrderModelAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'vendor']
    ordering = ("po_number", )


@admin.register(HistoricalPerformanceModel)
class HistoricalPerformanceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'date']
    ordering = ['id']