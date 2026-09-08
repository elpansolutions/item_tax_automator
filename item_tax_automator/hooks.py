app_name = "item_tax_automator"
app_title = "Item Tax Automator"
app_publisher = "Frappe"
app_description = "Auto manage In-State and Out-State Item Taxes"
app_email = "frappe@example.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "item_tax_automator",
# 		"logo": "/assets/item_tax_automator/logo.png",
# 		"title": "Item Tax Automator",
# 		"route": "/item_tax_automator",
# 		"has_permission": "item_tax_automator.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/item_tax_automator/css/item_tax_automator.css"
# app_include_js = "/assets/item_tax_automator/js/item_tax_automator.js"

# include js, css files in header of web template
# web_include_css = "/assets/item_tax_automator/css/item_tax_automator.css"
# web_include_js = "/assets/item_tax_automator/js/item_tax_automator.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "item_tax_automator/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Item": "public/js/item_tax_controller.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item": {
		"validate": "item_tax_automator.item_tax_automator.item_events.auto_populate_item_taxes"
	}
}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "item_tax_automator/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "item_tax_automator.utils.jinja_methods",
# 	"filters": "item_tax_automator.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "item_tax_automator.install.before_install"
# after_install = "item_tax_automator.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "item_tax_automator.uninstall.before_uninstall"
# after_uninstall = "item_tax_automator.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "item_tax_automator.utils.before_app_install"
# after_app_install = "item_tax_automator.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "item_tax_automator.utils.before_app_uninstall"
# after_app_uninstall = "item_tax_automator.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "item_tax_automator.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "item_tax_automator.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"item_tax_automator.tasks.all"
# 	],
# 	"daily": [
# 		"item_tax_automator.tasks.daily"
# 	],
# 	"hourly": [
# 		"item_tax_automator.tasks.hourly"
# 	],
# 	"weekly": [
# 		"item_tax_automator.tasks.weekly"
# 	],
# 	"monthly": [
# 		"item_tax_automator.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "item_tax_automator.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "item_tax_automator.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "item_tax_automator.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "item_tax_automator.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["item_tax_automator.utils.before_request"]
# after_request = ["item_tax_automator.utils.after_request"]

# Job Events
# ----------
# before_job = ["item_tax_automator.utils.before_job"]
# after_job = ["item_tax_automator.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"item_tax_automator.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

