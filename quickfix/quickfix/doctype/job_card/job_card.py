# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def before_insert(self):
		if not self.labour_charge:
			self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")

	def validate(self):
		for items in self.parts_used:
			items.total_price = items.unit_price * items.quantity
		self.parts_total = sum((item.total_price) for item in self.parts_used)
		self.final_amount = self.parts_total + self.labour_charge
