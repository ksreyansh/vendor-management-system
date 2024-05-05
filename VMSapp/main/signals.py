from django.db.models.functions import Cast
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg, ExpressionWrapper, F, fields

from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel


def response_time(instance):
    vendor = instance.vendor

    # Average Response Time
    avg_time_difference_seconds = PurchaseOrderModel.objects.filter(
        vendor=vendor, status="COMPLETED"
    ).aggregate(
        avg_time_difference_seconds=Avg(
            Cast(F('acknowledgement_date') - F('issue_date'), fields.FloatField())
        )
    )['avg_time_difference_seconds']
    average_time_difference_seconds = round(avg_time_difference_seconds / 86400, 2) if avg_time_difference_seconds else 0

    # Update or create VendorModel
    inst_vendor, created = VendorModel.objects.get_or_create(vendor_code=instance.vendor.vendor_code)
    inst_vendor.average_response_time = average_time_difference_seconds
    inst_vendor.save()


@receiver(post_save, sender=PurchaseOrderModel)
def calculate_average_response_time(sender, instance, **kwargs):
    if instance.pk:
        if instance.acknowledgement_date:
            response_time(instance)


# Performance Metrics calculation
@receiver(post_save, sender=PurchaseOrderModel)
def calculate_performance_metrics(sender, instance, created, **kwargs):
    if instance.status == "COMPLETED":
        vendor = instance.vendor

        # Update completion time
        instance.completion_date = timezone.now()
        instance.save()

        # On-time Delivery Rate
        completed_pos_count = PurchaseOrderModel.objects.filter(
            vendor=vendor,
            status='COMPLETED',
            completion_date__lte=instance.delivery_date
        ).count()
        total_completed_pos_count = PurchaseOrderModel.objects.filter(vendor=vendor, status="COMPLETED").count()
        on_time_delivery_rate = completed_pos_count / total_completed_pos_count if total_completed_pos_count else total_completed_pos_count

        # Quality Rating Average
        rating_avg = PurchaseOrderModel.objects.filter(vendor=vendor).aggregate(
            average_rating=Avg('quality_rating', default=0)
        )['average_rating']

        # Average Response Time
        avg_time_difference_seconds = PurchaseOrderModel.objects.filter(
            vendor=vendor, status="COMPLETED"
        ).aggregate(
            avg_time_difference_seconds=Avg(
                Cast(F('acknowledgement_date') - F('issue_date'), fields.FloatField())
            )
        )['avg_time_difference_seconds']
        average_time_difference_seconds = round(avg_time_difference_seconds / 86400, 2) if avg_time_difference_seconds else 0

        # Fulfillment Rate
        num_pos_completed = PurchaseOrderModel.objects.filter(vendor=vendor, status="COMPLETED").count()
        num_pos_issued = PurchaseOrderModel.objects.filter(vendor=vendor).count()
        fulfill_rate = num_pos_completed / num_pos_issued if num_pos_issued else 0

        # Update or create HistoricalPerformanceModel record
        record, _ = HistoricalPerformanceModel.objects.get_or_create(
            vendor=instance.vendor,
            date=timezone.now(),
            defaults={
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': rating_avg,
                'average_response_time': average_time_difference_seconds,
                'fulfillment_rate': fulfill_rate
            }
        )
        if not _:
            record.on_time_delivery_rate = on_time_delivery_rate
            record.quality_rating_avg = rating_avg
            record.average_response_time = average_time_difference_seconds
            record.fulfillment_rate = fulfill_rate
            record.save()

        # Update VendorModel
        inst_vendor, _ = VendorModel.objects.get_or_create(vendor_code=instance.vendor.vendor_code)
        inst_vendor.on_time_delivery_rate = on_time_delivery_rate
        inst_vendor.quality_rating_avg = rating_avg
        inst_vendor.average_response_time = average_time_difference_seconds
        inst_vendor.fulfillment_rate = fulfill_rate
        inst_vendor.save()
