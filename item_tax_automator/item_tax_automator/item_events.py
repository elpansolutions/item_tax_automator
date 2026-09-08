# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cint, flt


def get_tax_automator_settings():
	"""Fetch settings with safe fallbacks."""
	try:
		settings = frappe.get_cached_doc("Item Tax Automator Settings")
		return {
			"enabled": cint(settings.get("enable_auto_item_tax", 1)),
			"in_state_category": settings.get("in_state_tax_category") or "In-State",
			"out_state_category": settings.get("out_state_tax_category") or "Out-State",
		}
	except Exception:
		return {
			"enabled": 1,
			"in_state_category": "In-State",
			"out_state_category": "Out-State",
		}


def auto_populate_item_taxes(doc, method=None):
	"""
	Hook called on Item validate/before_save.
	Safely ensures that:
	1. If a tax row has a template but no category, it defaults to in-state category.
	2. If an in-state row exists for a template, the paired out-state row is automatically added.
	3. Prevent duplicate entries (fully idempotent).
	"""
	settings = get_tax_automator_settings()
	if not settings["enabled"]:
		return

	if not doc.get("taxes"):
		return

	in_state = settings["in_state_category"]
	out_state = settings["out_state_category"]

	# Pass 1: Set default in-state category on rows with missing tax category
	for row in doc.taxes:
		if row.item_tax_template and not row.tax_category:
			row.tax_category = in_state

	# Pass 2: Track existing (template, category) pairs
	existing_pairs = set()
	for row in doc.taxes:
		if row.item_tax_template and row.tax_category:
			existing_pairs.add((row.item_tax_template, row.tax_category))

	# Pass 3: Identify missing out-state rows (and missing in-state rows)
	rows_to_add = []
	for row in list(doc.taxes):
		if not row.item_tax_template:
			continue

		template = row.item_tax_template

		# If in-state exists, check if out-state is missing
		if row.tax_category == in_state and (template, out_state) not in existing_pairs:
			rows_to_add.append({
				"item_tax_template": template,
				"tax_category": out_state,
				"valid_from": row.valid_from,
				"minimum_net_rate": flt(row.minimum_net_rate),
				"maximum_net_rate": flt(row.maximum_net_rate),
			})
			existing_pairs.add((template, out_state))

		# If out-state exists, check if in-state is missing
		elif row.tax_category == out_state and (template, in_state) not in existing_pairs:
			rows_to_add.append({
				"item_tax_template": template,
				"tax_category": in_state,
				"valid_from": row.valid_from,
				"minimum_net_rate": flt(row.minimum_net_rate),
				"maximum_net_rate": flt(row.maximum_net_rate),
			})
			existing_pairs.add((template, in_state))

	# Pass 4: Append new rows to doc.taxes child table
	for new_row_data in rows_to_add:
		doc.append("taxes", new_row_data)


@frappe.whitelist()
def get_paired_tax_category_data(template, current_category=None):
	"""
	Helper for Client Script to quickly get complementary tax category data.
	"""
	settings = get_tax_automator_settings()
	if not settings["enabled"]:
		return None

	in_state = settings["in_state_category"]
	out_state = settings["out_state_category"]

	if not current_category or current_category == in_state:
		return {
			"primary_category": in_state,
			"secondary_category": out_state,
		}
	elif current_category == out_state:
		return {
			"primary_category": out_state,
			"secondary_category": in_state,
		}

	return None
