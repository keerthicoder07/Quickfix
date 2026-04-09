import frappe
import frappe.utils as fu


def apply_all():
	_patch_get_url()


def _patch_get_url():
	if hasattr(fu, "_qf_patched"):
		return
	_orig = fu.get_url

	def _custom_get_url(path=None, full_address=False):
		url = _orig(path, full_address)
		prefix = frappe.conf.get("custom_url_prefix", "")
		return prefix + url if prefix else url

	fu.get_url = _custom_get_url
	fu._qf_patched = True
