import frappe


def boot_session(bootinfo):
	"""Inject Galaxy brand tokens into every desk session."""
	bootinfo.galaxy_brand = {
		"product_name": "Galaxy",
		"vendor": "eKosmos Inc.",
		"tagline": "AI-first PSA for MSP/MSSPs",
		"support_email": "support@ekosmos.com",
		"logo": "/assets/galaxy_psa/images/galaxy-logo.svg",
		"favicon": "/assets/galaxy_psa/images/galaxy-favicon.svg",
	}
	# Override the desk's app title so it reads "Galaxy" instead of "Frappe"
	bootinfo.app_name = "Galaxy"
