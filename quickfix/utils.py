import frappe
from frappe import _


def validate_job_card(doc, method):
	if doc.priority == "Urgent" and not doc.assigned_technician:
		frappe.throw(_("Assign technician (doc_events)"))


def get_shop_name():
	return frappe.db.get_single_value("QuickFix Settings", "shop_name")


def format_job_id(value):
	return f"JOB#{value}"
