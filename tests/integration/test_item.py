from datetime import datetime

from quickbooks.objects.account import Account
from quickbooks.objects.item import Item
from tests.integration.test_base import QuickbooksTestCase


class ItemTest(QuickbooksTestCase):
    def setUp(self):
        super(ItemTest, self).setUp()

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Item {0}".format(self.account_number)

        self.income_account = Account.where(
            "AccountType = 'Income' and AccountSubType = 'SalesOfProductIncome'", max_results=1, qb=self.qb_client)[0]

        self.expense_account = Account.where(
            "AccountSubType = 'SuppliesMaterialsCogs'", max_results=1, qb=self.qb_client)[0]
        self.asset_account = Account.where("AccountSubType = 'Inventory'", max_results=1, qb=self.qb_client)[0]

    def test_create(self):
        item = Item()

        item.Name = self.name
        item.Type = "Inventory"
        item.TrackQtyOnHand = True
        item.QtyOnHand = 10
        item.Sku = "SKU123123"
        item.InvStartDate = "2015-01-01"

        item.IncomeAccountRef = self.income_account.to_ref()
        item.ExpenseAccountRef = self.expense_account.to_ref()
        item.AssetAccountRef = self.asset_account.to_ref()
        item.save(qb=self.qb_client)

        query_item = Item.get(item.Id, qb=self.qb_client)

        self.assertEqual(query_item.Id, item.Id)
        self.assertEqual(query_item.Name, self.name)
        self.assertEqual(query_item.Type, "Inventory")
        self.assertEqual(query_item.Sku, "SKU123123")
        self.assertEqual(query_item.TrackQtyOnHand, True)
        self.assertEqual(query_item.QtyOnHand, 10)
        self.assertEqual(query_item.IncomeAccountRef.value, self.income_account.Id)
        self.assertEqual(query_item.ExpenseAccountRef.value, self.expense_account.Id)
        self.assertEqual(query_item.AssetAccountRef.value, self.asset_account.Id)
