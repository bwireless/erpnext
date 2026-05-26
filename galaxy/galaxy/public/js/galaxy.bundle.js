// Galaxy desk-side JS entry. Bundle target for hooks.app_include_js.
// Real client logic (ticket actions, SLA UI, AI agent console) will be
// added as the corresponding modules are built out.

frappe.provide("galaxy");

galaxy.version = "0.0.1";

frappe.ready?.(() => {
    console.info("[galaxy] desk bundle loaded", galaxy.version);
});
