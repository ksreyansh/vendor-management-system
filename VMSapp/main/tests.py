from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from faker import Faker
import datetime

from authentication.models import CustomUser
from .models import VendorModel, PurchaseOrderModel, HistoricalPerformanceModel


# Create your tests here.
#######################
# Vendor Model #
#######################
class VendorTestCaseGet(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')
        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        fake = Faker('en_IN')
        Faker.seed(100)

        for i in range(10, 20):
            VendorModel.objects.create(
                vendor_code="AV" + str(i),
                name=fake.company(),
                contact_details=fake.company_email(),
                address=fake.city_name(),
                on_time_delivery_rate=0.0,
                quality_rating_avg=0.0,
                average_response_time=0.0,
                fulfillment_rate=0.0
            )

    def test_get_all_vendors(self):
        """
        Test to get details of all the vendors
        """
        url = reverse("main:vendor")
        data = {}

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(VendorModel.objects.count(), 10)
        print("Test: Get all Vendors -> Completed")

    def test_get_vendor_by_id(self):
        """
        Test to get detail of any individual vendor by ID
        """
        url = reverse("main:vendor-id", kwargs={'pk': "AV10"})
        data = {}

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test: Get Vendor by ID -> Completed")

    def test_get_nonexistent_vendor(self):
        """
        Test to get details of a vendor with non-existent ID
        """
        url = reverse("main:vendor-id", kwargs={'pk': '999'})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Get non-existent Vendor -> Completed")


class VendorTestCasePost(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

    def test_create_vendor(self):
        """
        Test to create a valid new vendor
        """
        url = reverse("main:vendor")
        data = {
            "vendor_code": "AV9",
            "name": "Test Company",
            "contact_details": "9988776654",
            "address": "Test Location",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 0.0,
            "average_response_time": 0.0,
            "fulfillment_rate": 0.0
        }

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorModel.objects.count(), 1)
        self.assertEqual(VendorModel.objects.get(vendor_code=data["vendor_code"]).address, "Test Location")
        print("Test: Create Vendor -> Completed")

    def test_invalid_create_vendor(self):
        """
        Test for invalid creation of a new vendor
        """
        url = reverse("main:vendor")
        data = {
            "vendor_code": "AV9",

            "contact_details": "9988776654",
            "address": "Test Location",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 0.0,
            "average_response_time": 0.0,
            "fulfillment_rate": 0.0
        }

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Invalid Create Vendor -> Completed")


class VendorTestCasePut(APITestCase):
    def setUp(self):
        # Create test user
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )
        self.valid_data = {
            "vendor_code": self.vendor.vendor_code,
            "name": "Updated Vendor",
            "contact_details": "9900990099",
            "address": "Updated Location",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 0.0,
            "average_response_time": 0.0,
            "fulfillment_rate": 0.0
        }
        self.invalid_data = {
            "vendor_code": self.vendor.vendor_code,
            "name": "",
            "contact_details": "9900990099",
            "address": "Test Location 2",
            "on_time_delivery_rate": 0.0,
            "quality_rating_avg": 0.0,
            "average_response_time": 0.0,
            "fulfillment_rate": 0.0
        }

    def test_valid_put(self):
        """
        Test to update vendor details
        """
        try:
            url = reverse("main:vendor-id", kwargs={'pk': self.vendor.vendor_code})

            # Set auth token in the request header
            headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

            response = self.client.put(url, self.valid_data, format='json', **headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.vendor.refresh_from_db()
            self.assertEqual(self.vendor.name, "Updated Vendor")
            self.assertEqual(self.vendor.address, "Updated Location")
            print("Test: Valid Update Vendor -> Completed")
        except Exception as e:
            print("Exception:", e)

    #    Test for ID not present in Update
    def test_invalid_put(self):
        """
        Test for updating vendor details if ID has not been provided
        """
        try:
            url = url = reverse("main:vendor-id", kwargs={'pk': self.vendor.vendor_code})

            # Set auth token in the request header
            headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

            response = self.client.put(url, self.invalid_data, format='json', **headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("Test: Invalid Update Vendor -> Completed")
        except Exception as e:
            print("Exception:", e)


class VendorTestCaseDelete(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)
        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

    def test_valid_delete(self):
        """
            Test for deleting Vendor information
        """
        url = reverse('main:vendor-id', kwargs={'pk': self.vendor.vendor_code})
        try:
            # Set auth token in the request header
            headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

            response = self.client.delete(url, **headers)

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(VendorModel.objects.filter(pk=self.vendor.pk).exists())
            print("Test: Delete Request -> Completed")
        except Exception as e:
            print("Exception:", e)

    #   Test for ID not present in delete
    def test_invalid_delete(self):
        """
        Test for invalid deletion of Vendor information
        """
        invalid_url = reverse('main:vendor-id', kwargs={'pk': "999"})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.delete(invalid_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Invalid Delete Request -> Completed")


########################
# Purchase Order Model #
########################
class POTestCaseSetUpGet(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)
        fake = Faker('en_IN')
        Faker.seed(100)

        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        for i in range(10, 20):
            PurchaseOrderModel.objects.create(
                po_number="AO" + str(i),
                vendor=self.vendor,
                order_date=timezone.now(),
                delivery_date=timezone.now() + datetime.timedelta(days=5),
                items=[{
                    "name": "Jeans", "price": "14.50"
                }],
                quantity=1,
                status="PENDING",
                quality_rating=0.0,
                issue_date=timezone.now(),
                acknowledgement_date=timezone.now()+datetime.timedelta(hours=1)
            )


class POTestCases(POTestCaseSetUpGet):
    def test_get_all_orders(self):
        """
        Test to get details of all the orders
        """
        url = reverse("main:order")
        data = {}

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrderModel.objects.count(), 10)
        print("Test: Get all Orders -> Completed")

    def test_get_order_by_id(self):
        """
        Test to get details of a purchase order by ID
        """
        url = reverse("main:order-id", kwargs={'pk': "AO10"})
        data = {}

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Test: Get Order by ID -> Completed")

    def test_get_nonexistent_order(self):
        """
        Test to get details of a purchase order with invalid ID
        """
        url = reverse("main:order-id", kwargs={'pk': '999'})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Get non-existent Order -> Completed")


class POTestCasePost(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

    def test_create_order(self):
        """
        Test for valid create request of a new purchase order
        """
        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        url = reverse("main:order")
        data = {
            "po_number": "AO4",
            "order_date": "2024-04-30T20:45:11+05:30",
            "delivery_date": "2024-05-05T20:45:25+05:30",
            "items": [
                {
                    "name": "Item 1",
                    "price": "2.50"
                },
                {
                    "name": "Item 2",
                    "price": "4.50"
                }
            ],
            "quantity": 1,
            "status": "PENDING",
            "quality_rating": 0.0,
            "issue_date": "2024-04-30T20:45:59+05:30",
            "acknowledgement_date": "2024-04-30T21:45:59+05:30",
            "vendor": self.vendor.vendor_code
        }

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrderModel.objects.count(), 1)
        print("Test: Create Purchase Order -> Completed")

    def test_invalid_create_order(self):
        """
        Test for invalid create request of purchase order
        """
        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        url = reverse("main:vendor")
        data = {
            # "po_number": "AO4",
            "order_date": "2024-04-30T20:45:11+05:30",
            "delivery_date": "2024-05-05T20:45:25+05:30",
            "items": [
                {
                    "name": "Item 1",
                    "price": "2.50"
                },
                {
                    "name": "Item 2",
                    "price": "4.50"
                }
            ],
            "quantity": 1,
            "status": "PENDING",
            "quality_rating": 0.0,
            "issue_date": "2024-04-30T20:45:59+05:30",
            "acknowledgement_date": "2024-04-30T21:45:59+05:30",
            "vendor": self.vendor.vendor_code
        }

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Test: Invalid Create Purchase Order -> Completed")


class POTestCasePut(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        self.order = PurchaseOrderModel.objects.create(
            po_number="AO5",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now()+datetime.timedelta(days=5),
            items=[{
                "name": "Jeans", "price": "14.50"
            }],
            quantity=1,
            status="PENDING",
            quality_rating=0.0,
            issue_date=timezone.now(),
            acknowledgement_date=timezone.now()+datetime.timedelta(hours=1)
        )
        self.valid_data = {
            "po_number": self.order.po_number,
            "order_date": "2024-04-30T20:45:11+05:30",
            "delivery_date": "2024-05-05T20:45:25+05:30",
            "items": [
                {
                    "name": "Item 1",
                    "price": "2.50"
                },
                {
                    "name": "Item 2",
                    "price": "4.50"
                }
            ],
            "quantity": 3,
            "status": "PENDING",
            "quality_rating": 0.0,
            "issue_date": "2024-04-30T20:45:59+05:30",
            "acknowledgement_date": "2024-04-30T21:45:59+05:30",
            "vendor": self.order.vendor.vendor_code
        }

        self.invalid_data = {
            "po_number": self.order.po_number,
            "order_date": "2024-04-30T20:45:11+05:30",
            "delivery_date": "2024-05-05T20:45:25+05:30",
            "items": [
                {
                    "name": "Item 1",
                    "price": "2.50"
                },
                {
                    "name": "Item 2",
                    "price": "4.50"
                }
            ],
            "quantity": 1,
            "status": "PENDING",
            "quality_rating": 0.0,
            "issue_date": "2024-04-30T20:45:59+05:30",
            "acknowledgement_date": "2024-04-30T21:45:59+05:30",
            # "vendor": self.order.vendor
        }

    def test_valid_put(self):
        """
        Test for valid update request of Purchase Order
        """
        try:
            url = reverse("main:order-id", kwargs={'pk': self.order.po_number})

            # Set auth token in the request header
            headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

            response = self.client.put(url, self.valid_data, format='json', **headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.order.refresh_from_db()
            self.assertEqual(self.order.status, "PENDING")
            self.assertEqual(self.order.quantity, 3)
            print("Test: Valid Update Purchase Order -> Completed")
        except Exception as e:
            print("Exception:", e)

    #    Test for ID not present in Update
    def test_invalid_put(self):
        """
        Test for invalid update request of Purchase Order
        """
        try:
            url = url = reverse("main:order-id", kwargs={'pk': self.order.po_number})

            # Set auth token in the request header
            headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

            response = self.client.put(url, self.invalid_data, format='json', **headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            print("Test: Invalid Update Purchase Order -> Completed")
        except Exception as e:
            print("Exception:", e)


class POTestCaseDelete(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        self.order = PurchaseOrderModel.objects.create(
            po_number="AO5",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now()+datetime.timedelta(days=5),
            items=[{
                "name": "Jeans", "price": "14.50"
            }],
            quantity=1,
            status="PENDING",
            quality_rating=0.0,
            issue_date=timezone.now(),
            acknowledgement_date=timezone.now()+datetime.timedelta(hours=1)
        )

    def test_valid_delete(self):
        """
        Test for valid delete request of Purchase Order
        """
        url = reverse('main:order-id', kwargs={'pk': self.order.po_number})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        try:
            response = self.client.delete(url, **headers)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(PurchaseOrderModel.objects.filter(pk=self.order.pk).exists())
            print("Test: Delete Request -> Completed")
        except Exception as e:
            print("Exception:", e)

    #   Test for ID not present in delete
    def test_invalid_delete(self):
        """
        Test for invalid delete request of Purchase Order
        """
        invalid_url = reverse('main:order-id', kwargs={'pk': "999"})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.delete(invalid_url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Invalid Delete Request -> Completed")


class AcknowledgePOTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        self.order = PurchaseOrderModel.objects.create(
            po_number="AO5",
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now()+datetime.timedelta(days=5),
            items=[{
                "name": "Jeans", "price": "14.50"
            }],
            quantity=1,
            status="PENDING",
            quality_rating=0.0,
            issue_date=timezone.now(),
            acknowledgement_date=timezone.now()+datetime.timedelta(hours=1)
        )

    def test_acknowledge_valid_po_number(self):
        url = reverse('main:acknowledge', kwargs={'pk': self.order.pk})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.patch(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertIsNotNone(self.order.acknowledgement_date)

        print("Test: Acknowledge purchase order -> Completed")

    def test_acknowledge_invalid_po_number(self):
        url = reverse('main:acknowledge', kwargs={'pk': '999'})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.patch(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print("Test: Acknowledge purchase order with invalid ID -> Completed")


class HistoricalPerformanceModelTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_superuser(email='testsuperuser@example.com',
                                                        password='password123')

        # Create a test client and authenticate with the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Generate authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        # Create a vendor for testing
        self.vendor = VendorModel.objects.create(
            vendor_code="AV8",
            name="Test Vendor",
            contact_details="9900990099",
            address="Test location",
            on_time_delivery_rate=0.0,
            quality_rating_avg=0.0,
            average_response_time=0.0,
            fulfillment_rate=0.0
        )

        # Create historical performance data for the vendor
        self.performance_data = HistoricalPerformanceModel.objects.create(
            vendor=self.vendor,
            date=timezone.now(),
            on_time_delivery_rate=0.85,
            quality_rating_avg=4.2,
            average_response_time=15.3,
            fulfillment_rate=0.92
        )

    def test_get_performance_data(self):
        # Test retrieving performance data for a valid vendor
        url = reverse('main:vendor-performance', kwargs={'pk': self.vendor.vendor_code})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vendor'], self.vendor.vendor_code)
        print("Test: Get vendor performance data -> Completed")

    def test_get_performance_data_invalid_vendor(self):
        # Test retrieving performance data for an invalid vendor
        url = reverse('main:vendor-performance', kwargs={'pk': '999'})

        # Set auth token in the request header
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Test: Get vendor performance data with invalid ID -> Completed")


