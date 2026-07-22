from maxauto_custom import __version__

app_name = "maxauto_custom"
app_title = "Max Auto Customizations"
app_publisher = "Max Auto Cables Pvt Ltd"
app_description = "MaxAuto Manufacturing Platform - Comprehensive ERP solution for rope/cable manufacturing, CNC machining, and multi-unit operations"
app_email = "info@maxautocables.com"
app_license = "MIT"
app_version = __version__

# Apps Screen - Register app for Desk sidebar
add_to_apps_screen = [
    {
        "name": app_name,
        "logo": "/assets/maxauto_custom/images/logo.svg",
        "title": "Maxauto",
        "route": "/app/maxauto",
    }
]

# Fixtures to load - Version controlled customizations
# Export with: bench --site <site> export-fixtures --app maxauto_custom
fixtures = [
	# Workspace
	{
		"dt": "Workspace",
		"filters": [["name", "in", ["Maxauto"]]],
	},
	# Custom Fields
	{
		"dt": "Custom Field",
		"filters": [["module", "=", "Maxauto"]],
	},
	# Property Setters
	{
		"dt": "Property Setter",
		"filters": [["module", "=", "Maxauto"]],
	},
	# Client Scripts
	{
		"dt": "Client Script",
		"filters": [["module", "=", "Maxauto"]],
	},
	# Server Scripts
	{
		"dt": "Server Script",
		"filters": [["module", "=", "Maxauto"]],
	},
	# Print Formats
	{
		"dt": "Print Format",
		"filters": [["module", "=", "Maxauto"]],
	},
	# Notifications
	{
		"dt": "Notification",
		"filters": [["module", "=", "Maxauto"]],
	},
]

# Custom Roles used by DocType permissions in this app.
# Created on install via before_install so permission rows are effective.
before_install = "maxauto_custom.setup.setup_roles"

# Desk
# Note: Desk menu items are added via Workspace shortcuts, not hooks