// Copyright (c) 2026, Aerele and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Job Card", {
// 	refresh(frm) {

// 	},
// });

frappe.realtime.on("job_ready", (data) => {
	console.log("Job ready:", data);
});
