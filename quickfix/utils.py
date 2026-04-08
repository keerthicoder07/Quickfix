import frappe
from frappe import _


def validate_job_card(doc, method):
	if doc.priority == "Urgent" and not doc.assigned_technician:
		frappe.throw(_("Assign technician (doc_events)"))
