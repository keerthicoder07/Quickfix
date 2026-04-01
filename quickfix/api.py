from datetime import timedelta

import frappe
from frappe.query_builder import DocType
from frappe.utils import now_datetime


@frappe.whitelist
def get_overdue_jobs():
	Jc = DocType("Job Card")
	seven_days = now_datetime - timedelta(days=7)
	result = (
		frappe.qb.from_(Jc)
		.select(Jc.name, Jc.customer_name, Jc.assigned_technician, Jc.creation)
		.where(Jc.status.isin("Pending Diagnosis", "In Repair") & (Jc.creation < seven_days))
		.Orderby(Jc.creation, order=frappe.qb.asc)
	).run(as_dict=True)
	return result


@frappe.whitelist
def transfer_job(from_tech, to_tech):
	try:
		frappe.db.sql(
			"""
        update `tabJob Card`
        set assigned_technician=%s
        Where assigned_technician=%s
        and status in('Pending Diagnosis','In Repair')
        """,
			(to_tech, from_tech),
		)
		frappe.db.commit()
		return {"status": "success", "message": f"Jobs transferred from {from_tech} to {to_tech}"}
	except Exception:
		frappe.db.rollback()
		frappe.log_error(title="Job transfer failed", message=frappe.get_traceaback())
		raise
