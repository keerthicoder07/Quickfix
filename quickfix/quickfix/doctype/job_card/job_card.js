// Copyright (c) 2026, Aerele and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Job Card", {
	setup: function (frm) {
		frm.set_query("assigned_technician", function () {
			return {
				filters: {
					status: "Active",
					specialization: frm.doc.device_type,
				},
			};
		});
	},
	refresh: function (frm) {
		frm.add_custom_button(__("Reject Job"), function () {
			let d = new frappe.ui.Dialog({
				title: __("Reject Job"),
				fields: [
					{
						label: "Rejection Reason",
						fieldname: "reason",
						fieldtype: "Small Text",
						reqd: 1,
					},
				],
				primary_action_label: __("Submit"),
				primary_action(values) {
					frappe.msgprint("Rejected: " + values.reason);
					d.hide();
				},
			});
			d.show();
		}),
			frm.add_custom_button(__("Transfer Technician"), function () {
				frappe.prompt(
					[
						{
							label: __("New Technician"),
							fieldname: "technician",
							fieldtype: "Link",
							options: "Technician",
							reqd: 1,
							get_query: function () {
								return {
									filters: {
										status: "Active",
										specialization: frm.doc.device_type,
									},
								};
							},
						},
					],
					function (values) {
						frappe.confirm("Are you sure want to transfer?", function () {
							frappe.call({
								method: "quickfix.api.transfer_job",
								args: {
									from_tech: frm.doc.assigned_technician,
									to_tech: values.technician,
								},
								callback: function () {
									frm.set_value("assigned_technician", values.technician);

									frm.trigger("asssigned_technician");
								},
							});
						});
					}
				);
			});
	},
});

frappe.realtime.on("job_ready", (data) => {
	console.log("Job ready:", data);
});
