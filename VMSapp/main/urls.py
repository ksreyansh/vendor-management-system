from django.urls import path

from .views import VendorAPIView, PurchaseOrderAPIView, AcknowledgePOAPIView, PerformanceDataAPIView

app_name = "main"

urlpatterns = [
    path('purchase_orders/<str:pk>/acknowledge/', AcknowledgePOAPIView.as_view(), name="acknowledge"),
    path('vendor/<str:pk>/performance/', PerformanceDataAPIView.as_view(), name="vendor-performance"),
    path('purchase_orders/<str:pk>/', PurchaseOrderAPIView.as_view(), name="order-id"),
    path('vendor/<str:pk>/', VendorAPIView.as_view(), name="vendor-id"),
    path('purchase_orders/', PurchaseOrderAPIView.as_view(), name="order"),
    path('vendor/', VendorAPIView.as_view(), name="vendor"),
]