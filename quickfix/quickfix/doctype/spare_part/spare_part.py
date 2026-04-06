# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SparePart(Document):
	def before_save(self):
		if self.unit_cost > self.selling_price:
			frappe.throw("Always selling price should greater than unit cost")
