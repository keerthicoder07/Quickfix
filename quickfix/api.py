from datetime import timedelta
from typing import Optional

import frappe
from frappe import _
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


@frappe.whitelist()
def transfer_job(from_tech: str, to_tech: str) -> None:
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


@frappe.whitelist()
def share_job_card(job_card_name: str, user_email: str) -> None:
	try:
		# Check if document exists
		if not frappe.db.exists("Job Card", job_card_name):
			frappe.throw("Job Card not found")

		# Check if user exists
		if not frappe.db.exists("User", user_email):
			frappe.throw("User not found")

		# Share the document
		frappe.share.add(
			doctype="Job Card",
			name=job_card_name,
			user=user_email,
			read=1,  # 👈 Read access
			write=0,
			share=0,
			everyone=0,
		)

		return {"status": "success", "message": f"Job Card {job_card_name} shared with {user_email}"}

	except Exception:
		frappe.log_error(title="Share Job Card Failed", message=frappe.get_traceback())
		raise


@frappe.whitelist()
def manager_only_action():
	frappe.only_for("QF Manager")

	return {"status": "success", "message": "You are authorized as QF Manager"}


@frappe.whitelist()
def get_job_card_permission_query_conditions(user: str | None = None) -> str | None:
	if not user:
		user = frappe.session.user

	roles = frappe.get_roles(user)

	if "QF Technician" in roles and "QF Manager" not in roles:
		return f"""
            `tabJob Card`.assigned_technician IN (
                SELECT name FROM `tabTechnician`
                WHERE user = {frappe.db.escape(user)}
            )
        """

	return None


@frappe.whitelist()
def get_job_cards_safe():
	user = frappe.session.user
	roles = frappe.get_roles(user)
	data = frappe.get_list("Job Card", fields="*")
	if "QF Manager" not in roles:
		for row in data:
			row.pop("customer_phone", None)
			row.pop("customer_email", None)
	return data
