import unittest

from quickbooks import QuickBooks
from quickbooks.objects.paymentmethod import PaymentMethod


class PaymentMethodTests(unittest.TestCase):
    def test_unicode(self):
        payment_method = PaymentMethod()
        payment_method.Name = "test"

        self.assertEqual(str(payment_method), "test")

    def test_valid_object_name(self):
        obj = PaymentMethod()
        client = QuickBooks()
        result = client.isvalid_object_name(obj.qbo_object_name)

        self.assertTrue(result)

    def test_to_ref(self):
        obj = PaymentMethod()
        obj.Name = "test"
        obj.Id = 12

        ref = obj.to_ref()

        self.assertEqual(ref.name, "test")
        self.assertEqual(ref.type, "PaymentMethod")
        self.assertEqual(ref.value, 12)
