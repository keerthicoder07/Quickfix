import frappe
from frappe.utils import now


def log_change(doc, method):
	if doc.doctype == "Audit Log":  # module doctype
		return
	meta = frappe.get_meta(doc.doctype)
	if meta.module != "QuickFix":
		return
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doc.doctype,
			"document_name": doc.name,
			"action": method,
			"user": frappe.session.user,
			"timestamp": now(),
		}
	).insert(ignore_permissions=True)
