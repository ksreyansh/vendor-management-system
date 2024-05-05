from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel
from .serializers import VendorModelSerializer, PurchaseOrderModelSerializer, HistoricalPerformanceModelSerializer


# Create your views here.

class VendorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Fetches vendor details: ID may or may not be provided
    def get(self, request, pk=None, format=None):
        sid = pk
        if sid is not None:
            try:
                vendor = VendorModel.objects.get(pk=sid)
                serializer = VendorModelSerializer(vendor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'msg': "Error: Invalid vendor_code"}, status=status.HTTP_404_NOT_FOUND)

        vendors = VendorModel.objects.all()
        serializer = VendorModelSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Creates a new vendor profile
    def post(self, request, format=None):
        serializer = VendorModelSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'Record created successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'Database integrity error: {}'.format(str(e))},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Updates a vendor profile: ID needs to be provided
    def put(self, request, pk=None, format=None):
        if pk is None:
            return Response({'msg': 'Error - No vendor_code provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = VendorModel.objects.get(pk=pk)
        except VendorModel.DoesNotExist:
            return Response({'msg': 'Error - Vendor record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorModelSerializer(record, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Vendor record updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a vendor profile: ID needs to be provided
    def delete(self, request, pk=None, format=None):
        if pk is None:
            return Response({'msg': 'Error - No vendor_code provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = VendorModel.objects.get(pk=pk)
            record.delete()
            return Response({'msg': 'Vendor record deleted'}, status=status.HTTP_204_NO_CONTENT)
        except VendorModel.DoesNotExist:
            return Response({'msg': 'Error - Vendor record not found'}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Fetches purchase order details. ID may or may not be provided
    def get(self, request, pk=None, format=None):
        sid = pk
        if sid is not None:
            try:
                order = PurchaseOrderModel.objects.get(pk=sid)
                serializer = PurchaseOrderModelSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response({'msg': "Error: Invalid po_number"}, status=status.HTTP_404_NOT_FOUND)

        orders = PurchaseOrderModel.objects.all()
        serializer = PurchaseOrderModelSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Creates a purchase order
    def post(self, request, format=None):
        serializer = PurchaseOrderModelSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()

                return Response({'msg': 'Record created successfully'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'error': 'Database integrity error: {}'.format(str(e))},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Updates a purchase order: ID needs to be provided
    def put(self, request, pk=None, format=None):
        if pk is None:
            return Response({'msg': 'Error - No po_number provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = PurchaseOrderModel.objects.get(pk=pk)
        except PurchaseOrderModel.DoesNotExist:
            return Response({'msg': 'Error - Purchase Order record not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchaseOrderModelSerializer(record, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Vendor record updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a purchase order: ID needs to be provided
    def delete(self, request, pk=None, format=None):
        if pk is None:
            return Response({'msg': 'Error - No po_number provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = PurchaseOrderModel.objects.get(pk=pk)
            record.delete()
            return Response({'msg': 'Purchase Order record deleted'}, status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrderModel.DoesNotExist:
            return Response({'msg': 'Error - Purchase Order record not found'}, status=status.HTTP_404_NOT_FOUND)


class AcknowledgePOAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Simulates a vendor acknowledging the purchase order.
    """
    When this api is called, acknowledgement gets recorded
    which triggers a post_save signal which calculates the 
    average response time (performance metric) of the vendor
    """

    def patch(self, request, pk=None):
        if pk is None:
            return Response({'msg': 'Error - Invalid po_number'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sid = pk
            record = PurchaseOrderModel.objects.get(pk=sid)
            serializer = PurchaseOrderModelSerializer(record, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save(acknowledgement_date=timezone.now())

                return Response({'msg': 'Acknowledgement received'}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'msg': "Error: Invalid po_number"}, status=status.HTTP_404_NOT_FOUND)


class PerformanceDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Fetches historical performance data for the vendor
    def get(self, request, pk, format=None):
        try:
            vendor = VendorModel.objects.get(vendor_code=pk)
            perf_record = HistoricalPerformanceModel.objects.filter(vendor=vendor)
            serializer = HistoricalPerformanceModelSerializer(perf_record, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'msg': "Error: Invalid vendor_code"}, status=status.HTTP_404_NOT_FOUND)
