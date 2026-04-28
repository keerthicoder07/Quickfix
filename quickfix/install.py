from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def after_install():
	make_property_setter(
		doctype="Job Card", fieldname="remarks", property="bold", value=1, property_type="Check"
	)
