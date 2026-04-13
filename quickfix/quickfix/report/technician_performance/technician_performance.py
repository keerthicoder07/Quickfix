# Copyright (c) 2026, Aerele and contributors
# For license information, please see license.txt
import frappe
from frappe.utils import date_diff, getdate


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns(filters):
	cols = [
		{"label": "Technician", "fieldname": "technician", "fieldtype": "Link", "options": "Technician"},
		{"label": "Total Jobs", "fieldname": "total_jobs", "fieldtype": "Int"},
		{"label": "Completed", "fieldname": "completed", "fieldtype": "Int"},
		{"label": "Avg Turnaround Days", "fieldname": "avg_turnaround_days", "fieldtype": "Int"},
		{"label": "Revenue", "fieldname": "revenue", "fieldtype": "currency"},
		{"label": "Completion Rate", "fieldname": "completion_rate", "fieldtype": "percent"},
	]
	for dt in frappe.get_all("Device Type", fields=["name"]):
		cols.append(
			{
				"label": dt.name,
				"fieldname": dt.name.lower().replace(" ", "_"),
				"fieldtype": "Int",
				"width": 100,
			}
		)
	return cols


def get_data(filters):
	conditions = {}
	if filters.get("technician"):
		conditions["assigned_technician"] = filters["technician"]
	jobs = frappe.get_list(
		"Job Card",
		fields=[
			"name",
			"assigned_technician",
			"status",
			"device_type",
			"creation",
			"delivery_date",
			"estimated_cost",
		],
		filters=conditions,
	)
	tech_map = {}
	for j in jobs:
		if filters.get("from_date") and getdate(j.creation) < getdate(filters.get("from_date")):
			continue
		if filters.get("to_date") and getdate(j.creation) > getdate(filters.get("to_date")):
			continue
		tech = j.assigned_technician or "Unassigned"
		if tech not in tech_map:
			tech_map[tech] = {
				"technician": tech,
				"total_jobs": 0,
				"completed": 0,
				"revenue": 0,
				"total_days": 0,
				"count_days": 0,
			}
		# print(tech_map[tech])
		row = tech_map[tech]
		row["total_jobs"] += 1
		if j.status == "For Delivery" or j.status == "Delivered" or j.status == "Ready":
			row["completed"] += 1
			row["revenue"] += j.estimated_cost or 0
			# print(j.delivery_date)

			if j.delivery_date:
				row["total_days"] += date_diff(j.delivery_date, j.creation)
				row["count_days"] += 1
				# print(row["total_days"])
				# print(row["count_days"])
		key = (j.device_type or "").lower().replace(" ", "_")
		row[key] = row.get(key, 0) + 1

	data = []
	# print(tech_map["avg_turnaround_days"])
	for row in tech_map.values():
		row["avg_turnaround_days"] = row["total_days"] / row["count_days"] if row["count_days"] else 0
		row["completion_rate"] = (row["completed"] / row["total_jobs"]) * 100 if row["total_jobs"] else 0
		data.append(row)
	return data


def get_chart(data):
	return {
		"data": {
			"labels": [d["technician"] for d in data],
			"datasets": [
				{"name": "Total Jobs", "values": [d["total_jobs"] for d in data]},
				{"name": "Completed", "values": [d["completed"] for d in data]},
			],
		},
		"type": "bar",
		"colors": ["#5e64ff", "#28a745"],
	}


def get_summary(data):
	total_jobs = sum(d["total_jobs"] for d in data)
	total_revenue = sum(d["revenue"] for d in data)
	best = max(data, key=lambda x: x["completion_rate"], default=None)
	return [
		{"label": "Total Jobs", "value": total_jobs, "indicator": "Blue"},
		{"label": "Total Revenue", "value": total_revenue, "indicator": "Green"},
		{"label": "Best Technician", "value": best["technician"] if best else "-", "indicator": "Orange"},
	]


def monthly_performance():
	frappe.enqueue("quickfix.api.generate_monthly_revenue_report", queue="long", timeout=600)
