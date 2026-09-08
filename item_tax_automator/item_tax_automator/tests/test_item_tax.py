# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from item_tax_automator.item_tax_automator.item_events import auto_populate_item_taxes, get_tax_automator_settings


class TestItemTaxAutomator(FrappeTestCase):
	def setUp(self):
		# Ensure settings are active and configured
		self.settings = frappe.get_doc("Item Tax Automator Settings")
		self.settings.enable_auto_item_tax = 1
		self.settings.in_state_tax_category = "In-State"
		self.settings.out_state_tax_category = "Out-State"
		self.settings.save(ignore_permissions=True)
		frappe.clear_cache(doctype="Item Tax Automator Settings")

		# Get an existing valid Item Tax Template and HSN Code
		self.template = frappe.db.get_value("Item Tax Template", {}, "name") or "GST 18% - RRS"
		self.hsn_code = frappe.db.get_value("Item", {"gst_hsn_code": ["!=", ""]}, "gst_hsn_code") or "62132000"

	def test_auto_tax_generation_without_category(self):
		"""Item with a tax template and no category gets In-State and Out-State paired rows."""
		item_code = f"_TEST_ITEM_AUTO_{frappe.generate_hash(length=6)}"
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": item_code,
			"item_name": "Test Item Auto Tax",
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"gst_hsn_code": self.hsn_code,
			"taxes": [
				{
					"item_tax_template": self.template,
					"tax_category": "",
				}
			]
		})
		item.insert(ignore_permissions=True)

		self.assertEqual(len(item.taxes), 2)
		categories = {row.tax_category for row in item.taxes}
		templates = {row.item_tax_template for row in item.taxes}

		self.assertEqual(categories, {"In-State", "Out-State"})
		self.assertEqual(templates, {self.template})

		# Re-saving must be idempotent (no extra rows added)
		item.save(ignore_permissions=True)
		item.reload()
		self.assertEqual(len(item.taxes), 2)

		# Clean up
		item.delete(ignore_permissions=True)

	def test_auto_tax_generation_with_in_state(self):
		"""Item with In-State gets paired with Out-State."""
		item_code = f"_TEST_ITEM_IN_{frappe.generate_hash(length=6)}"
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": item_code,
			"item_name": "Test Item In State",
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"gst_hsn_code": self.hsn_code,
			"taxes": [
				{
					"item_tax_template": self.template,
					"tax_category": "In-State",
				}
			]
		})
		item.insert(ignore_permissions=True)

		self.assertEqual(len(item.taxes), 2)
		categories = {row.tax_category for row in item.taxes}
		self.assertEqual(categories, {"In-State", "Out-State"})

		item.delete(ignore_permissions=True)

	def test_already_paired_no_duplicates(self):
		"""Item with both In-State and Out-State does not add duplicates."""
		item_code = f"_TEST_ITEM_PAIR_{frappe.generate_hash(length=6)}"
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": item_code,
			"item_name": "Test Item Pair",
			"item_group": "All Item Groups",
			"stock_uom": "Nos",
			"gst_hsn_code": self.hsn_code,
			"taxes": [
				{
					"item_tax_template": self.template,
					"tax_category": "In-State",
				},
				{
					"item_tax_template": self.template,
					"tax_category": "Out-State",
				}
			]
		})
		item.insert(ignore_permissions=True)

		self.assertEqual(len(item.taxes), 2)
		item.save(ignore_permissions=True)
		item.reload()
		self.assertEqual(len(item.taxes), 2)

		item.delete(ignore_permissions=True)


def run_manual_test():
	"""Manual test execution helper."""
	test = TestItemTaxAutomator()
	test.setUp()
	test.test_auto_tax_generation_without_category()
	test.test_auto_tax_generation_with_in_state()
	test.test_already_paired_no_duplicates()
	print("ALL ITEM TAX AUTOMATOR TESTS PASSED SUCCESSFULLY!")
