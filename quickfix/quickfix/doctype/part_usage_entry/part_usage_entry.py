# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PartUsageEntry(Document):
	def validate(self):
		self.total_price = self.unit_price * self.quantity
