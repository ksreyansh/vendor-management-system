import re

from rest_framework import serializers

from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel


class VendorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = "__all__"

    # Validations

    # Validation rules for field name
    def validate_name(self, value):
        """
        Validate the 'name' field to ensure it includes all alphabets, numbers,
        and special characters: _, /, ., and blank space.
        """
        # Define a regular expression pattern to match the allowed characters
        pattern = r'^[a-zA-Z0-9_/.\s]+$'

        # Check if the value matches the pattern
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Name must include alphabets, numbers, and special characters: _, /, ., and blank space.")

        return value

    # Validation rules for field contact details: Phone number
    def validate_contact_details(self, value):
        """
        Validate the 'contact_details' field to ensure it includes all numbers up to 15 digits
        and special characters: (, ), +.
        """
        # Define a regular expression pattern to match the allowed characters
        pattern = r'^[\d()+]{1,15}$'

        # Check if the value matches the pattern
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Contact details must include numbers up to 15 digits and special characters: (, ), +.")

        return value

    # Validation rules for field address
    def validate_address(self, value):
        """
        Validate the 'address' field to ensure it contains all alphanumeric characters,
        and special characters: blank space, comma, full stop, /, (, ).
        """
        # Define a regular expression pattern to match the allowed characters
        pattern = r'^[a-zA-Z0-9\s,.()/]+$'

        # Check if the value matches the pattern
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Address must contain alphanumeric characters and special characters: blank space, comma, full stop, "
                "/, (, ).")

        return value


class PurchaseOrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderModel
        fields = "__all__"


class HistoricalPerformanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformanceModel
        fields = "__all__"
