import base64
from datetime import timedelta
from io import BytesIO
from typing import Optional

import frappe
import qrcode
from frappe import _
from frappe.client import get_count
from frappe.query_builder import DocType
from frappe.utils import get_last_day, getdate, now, now_datetime, nowdate


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
	if from_tech == to_tech:
		frappe.throw(_("Can't set already assigned technician"))
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
			frappe.throw(_("Job Card not found"))

		# Check if user exists
		if not frappe.db.exists("User", user_email):
			frappe.throw(_("User not found"))

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


@frappe.whitelist()
def send_job_ready_email(job_card: str, user: str, customer_email: str) -> None:
	email = frappe.db.get_value("User", user, "email")

	if not email:
		return
	frappe.sendmail(
		recipients=[email, customer_email],
		subject=("Your Job is Ready"),
		message=(f"Your jobcard {job_card} is ready for delivery"),
		attachments=[
			{
				"fname": f"{job_card}.pdf",
				"fcontent": frappe.get_print(
					doctype="Job Card", name=job_card, print_format="Job Card Reciept", as_pdf=True
				),
			}
		],
	)


@frappe.whitelist()
def rename_technician(old_name: str, new_name: str) -> None:
	if not frappe.db.exists("Technician", old_name):
		frappe.throw(_("Old Technician not found"))
	if frappe.db.exists("Technician", new_name):
		frappe.throw(_("New Technician already exists"))
	frappe.rename_doc(
		"Technician", old_name, new_name, merge=False
	)  # When we give merge=True then whether there is document with the new name where that data will be overwite in the old name document so the data will loss


@frappe.whitelist()
def custom_get_count(
	doctype: str,
	filters: dict | list | None = None,
	debug: bool = False,
	cache: bool = False,
) -> str:
	# print("Override called")
	frappe.get_doc(
		{
			"doctype": "Audit Log",
			"doctype_name": doctype,
			"action": "count_queried",
			"user": frappe.session.user,
			"timestamp": now(),
		}
	).insert(
		ignore_permissions=True
	)  # Here the ignore_permission is valid since it is the system process so whenever the doctype changes for events it will automatically saves so it is acceptable and not user initiated process
	# frappe.db.commit()
	count = get_count(doctype, filters, debug, cache)
	return f"Total_count={count}"


@frappe.whitelist()
def get_shop_name():
	return frappe.db.get_single_value("Quickfix Settings", "shop_name")


@frappe.whitelist()
def get_qr_code(name: str) -> str:
	url = f"/app/job-card/{name}"
	qr = qrcode.make(url)
	buffer = BytesIO()
	qr.save(buffer, format="PNG")
	encoded = base64.b64encode(buffer.getvalue()).decode()
	return f"data:image/png;base64,{encoded}"


@frappe.whitelist()
def generate_monthly_revenue_report(year: int):
	try:
		months = range(1, 13)
		total_year_revenue = 0
		for i, month in enumerate(months, 1):
			from_date = f"{year}--{month:02d}-01"
			to_date = frappe.utils.get_last_day(from_date)
			jobs = frappe.get_all(
				"Job Card",
				filters={"status": "Delivered", "delivery_date": ["between", [from_date, to_date]]},
				fields=["estimated_cost"],
			)
			monthly_revenue = sum(j.estimated_cost or 0 for j in jobs)
			total_year_revenue += monthly_revenue
			frappe.publish_progress(
				percent=round(i / 12 * 100),
				title="Generating Revenue Report",
				description=f"processing month{month}...",
			)
		frappe.logger().info(f"Total Revenue for {year}:{total_year_revenue}")
		return {"status": "success", "year": year, "total_revenue": total_year_revenue}
	except Exception:
		frappe.log_error(title="Yearly Revenue Report Failed", message=frappe.get_traceback())

		raise  # Exception("simulated failure testing")


@frappe.whitelist()
def monthly_performance(year: int):
	frappe.enqueue("quickfix.api.generate_monthly_revenue_report", queue="long", timeout=600, year=2026)
	return "Job queued"


# @frappe.whitelist(allow_guest=True)
# def get_job_summary():
# 	job_card_name = frappe.form_dict.get("job_card_name")

# 	if not job_card_name:
# 		frappe.local.response["http_status_code"] = 400
# 		return {"error": _("job_card_name is required")}

# 	if not frappe.db.exists("Job Card", job_card_name):
# 		frappe.local.response["http_status_code"] = 404
# 		return {"error": _("Not found")}

# 	job = frappe.get_value(
# 		"Job Card",
# 		job_card_name,
# 		["name", "customer_name", "status", "estimated_cost", "creation"],
# 		as_dict=True,
# 	)
# 	job["today_date"] = getdate()
# 	return job


# RATE_LIMIT = 2


# @frappe.whitelist(allow_guest=True)
# def get_job_by_phone():
# 	ip = frappe.local.request_ip or "unknown"
# 	current_minute = now_datetime().strftime("%Y-%m-%d-%H-%M")
# 	cache_key = f"rate_limit:{ip}:{current_minute}"
# 	count = frappe.cache().incr(cache_key)

# 	if count == 1:
# 		frappe.cache().expire(cache_key, 60)
# 	if count > RATE_LIMIT:
# 		frappe.local.response["http_status_code"] = 429
# 		return {"error": _("Too many requests.Try again later")}
# 	phone = frappe.form_dict.get("phone")
# 	if not phone:
# 		frappe.local.response["http_status_code"] = 400
# 		return {"error": _("phone is required")}
# 	job = frappe.get_value("Job Card", {"Customer_phone": phone}, ["name", "status"], as_dict=True)
# 	return job or {"message": _("No job found")}
