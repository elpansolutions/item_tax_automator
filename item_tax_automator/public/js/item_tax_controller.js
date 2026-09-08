// Copyright (c) 2026, Frappe and contributors
// For license information, please see license.txt

frappe.provide("item_tax_automator");

item_tax_automator.get_settings = function() {
	if (item_tax_automator._settings_cache) {
		return Promise.resolve(item_tax_automator._settings_cache);
	}
	return frappe.db.get_single_value("Item Tax Automator Settings", "enable_auto_item_tax").then((enabled) => {
		if (enabled === 0) {
			item_tax_automator._settings_cache = { enabled: false };
			return item_tax_automator._settings_cache;
		}
		return Promise.all([
			frappe.db.get_single_value("Item Tax Automator Settings", "in_state_tax_category"),
			frappe.db.get_single_value("Item Tax Automator Settings", "out_state_tax_category")
		]).then(([in_state, out_state]) => {
			item_tax_automator._settings_cache = {
				enabled: true,
				in_state: in_state || "In-State",
				out_state: out_state || "Out-State"
			};
			return item_tax_automator._settings_cache;
		});
	}).catch(() => {
		item_tax_automator._settings_cache = {
			enabled: true,
			in_state: "In-State",
			out_state: "Out-State"
		};
		return item_tax_automator._settings_cache;
	});
};

frappe.ui.form.on("Item Tax", {
	item_tax_template: function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row || !row.item_tax_template) return;

		item_tax_automator.get_settings().then((settings) => {
			if (!settings.enabled) return;

			const in_state = settings.in_state;
			const out_state = settings.out_state;

			// If current row has no tax category, default to in_state
			if (!row.tax_category) {
				frappe.model.set_value(cdt, cdn, "tax_category", in_state);
			}

			const current_category = row.tax_category || in_state;
			const paired_category = current_category === in_state ? out_state : (current_category === out_state ? in_state : null);

			if (!paired_category) return;

			// Check if paired row already exists in taxes child table
			const taxes = frm.doc.taxes || [];
			const exists = taxes.some(
				(r) => r.item_tax_template === row.item_tax_template && r.tax_category === paired_category
			);

			if (!exists) {
				const child = frm.add_child("taxes", {
					item_tax_template: row.item_tax_template,
					tax_category: paired_category,
					valid_from: row.valid_from || null,
					minimum_net_rate: row.minimum_net_rate || 0,
					maximum_net_rate: row.maximum_net_rate || 0
				});
				frm.refresh_field("taxes");
			}
		});
	}
});
