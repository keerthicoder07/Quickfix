import re

import frappe


def get_context(context):
	phone = frappe.form_dict.get("phone")
	context.jobs = []
	context.phone = phone
	context.title = "Track Job Status"
	context.description = "Track your job status using your phone number"
	context.og_title = "QuickFix Job Tracking"

	if phone:
		phone = re.sub(r"\D", "", phone)
		context.jobs = frappe.get_all(
			"Job Card", filters={"customer_phone": phone}, fields=["name", "status"]
		)
	return context
