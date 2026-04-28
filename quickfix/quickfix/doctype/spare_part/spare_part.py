# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SparePart(Document):
	def validate(self):
		if self.unit_cost >= self.selling_price:
			frappe.throw("Always selling price should greater than unit cost")

	def autoname(self):
		if self.part_code:
			self.part_code = self.part_code.upper()
		self.name = frappe.model.naming.make_autoname("Sp-.YYYY.-.#####")
