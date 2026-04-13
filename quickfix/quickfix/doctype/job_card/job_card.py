# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		if len(self.customer_phone) != 10:
			frappe.throw(_("Invalid Phone Number"))
		if not self.labour_charge:
			self.labour_charge = frappe.db.get_single_value("QuickFix Settings", "default_labour_charge")
		for items in self.parts_used:
			items.total_price = items.unit_price * items.quantity
		self.parts_total = sum((item.total_price) for item in self.parts_used)
		self.final_amount = self.parts_total + self.labour_charge
		reserved_status = [
			"In Repair",
			"Pending Diagnosis",
			"Awaiting Customer Approval",
			"Ready",
			"For Deleivery",
		]
		if self.status in reserved_status and not self.assigned_technician:
			frappe.throw(_("You must assign the Technician"))

	def before_submit(self):
		if self.status != "For Delivery":
			frappe.throw(_("You can submit only during the Delivery"))
		for item in self.parts_used:
			qty = frappe.db.get_value("Spare Part", {item.part_name == "part_name"}, "stock_qty")
			if item.quantity > qty:
				frappe.throw(_("Stock is not available"))

	def on_submit(self):
		for item in self.parts_used:
			qty = frappe.db.get_value("Spare Part", {"part_name": item.part_name}, "stock_qty")
			name = frappe.db.get_value("Spare Part", {"part_name": item.part_name}, "name")
			frappe.db.set_value("Spare Part", name, "stock_qty", qty - item.quantity)
			# doc = frappe.get_doc("Spare Part",name)
			# doc.save(ignore_permissions=True)
		invoice = frappe.get_doc(
			{
				"doctype": "Service Invoice",
				"job_card": self.name,
				"customer_name": self.customer_name,
				"invoice_date": self.delivery_date,
				"labour_charge": self.labour_charge,
				"parts_total": self.parts_total,
				"total_amount": self.final_amount,
				"payment_status": self.payment_status,
			}
		)
		invoice.insert(ignore_permissions=True)
		invoice.submit()
		frappe.publish_realtime("job_ready", {"job_card": self.name, "status": self.status}, user=self.owner)
		frappe.enqueue(
			"quickfix.api.send_job_ready_email",
			queue="default",
			job_card=self.name,
			user=self.owner,
			customer_email=self.customer_email,
		)

	def on_cancel(self):
		frappe.db.set_value("Job Card", self.name, "status", "Cancelled")
		for item in self.parts_used:
			qty = frappe.db.get_value("Spare Part", {"part_name": item.part_name}, "stock_qty")
			frappe.db.set_value("Spare Part", {"part_name": item.part_name}, "stock_qty", qty + item.quantity)
		# in_name=frappe.db.get_value("Service Invoice",{"job_card":self.name},"name")
		# doc=frappe.get_doc(in_name)
		# if doc.status==1:
		# 	doc.cancel()

	def on_trash(self):
		if self.status != "Cancelled" and self.status != "Draft":
			frappe.throw(_("Cannot delete the job in progress"))

	def before_print(self, print_settings=None):
		self.print_summary = f"{self.customer_name}-{self.device_brand} {self.device_model}"
