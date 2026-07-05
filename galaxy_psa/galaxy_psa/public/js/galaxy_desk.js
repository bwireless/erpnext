// Galaxy desk shell: retitle browser tab, hook into route changes.
frappe.after_ajax(() => {
	try {
		document.title = "Galaxy · eKosmos";
		const b = frappe.boot && frappe.boot.galaxy_brand;
		if (b && b.logo) {
			const img = document.querySelector(".navbar-brand img");
			if (img) img.src = b.logo;
		}
	} catch (e) {
		console.warn("[galaxy] boot rebrand failed", e);
	}
});
