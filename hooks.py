app_name = "maxauto_custom"
app_title = "Max Auto Customizations"
app_publisher = "Max Auto Cables Pvt Ltd"
app_description = "MaxAuto Manufacturing Platform - Comprehensive ERP solution for rope/cable manufacturing, CNC machining, and multi-unit operations"
app_email = "info@maxautocables.com"
app_license = "MIT"
app_version = "1.0.0"

# Modules
default_settings = {
	"maxauto_custom-max-auto-setup": 1
}

# Pages
page_list = [
	{
		"page_name": "asset-label-sheet",
		"title": "Asset Label Sheet",
		"icon": "fa fa-barcode"
	}
]

# DocTypes registered via folders - auto-discovered from maxauto/*/doctypes/*/

# Custom Fields (if needed)
# custom_fields = {}

# Document Hooks
doc_events = {
	"Manufacturing Routing": {
		"validate": "maxauto_custom.maxauto.manufacturing.doctypes.manufacturing_routing.manufacturing_routing.ManufacturingRouting.validate",
		"on_submit": "maxauto_custom.maxauto.manufacturing.doctypes.manufacturing_routing.manufacturing_routing.ManufacturingRouting.on_submit"
	},
	"Machine": {
		"validate": "maxauto_custom.maxauto.manufacturing.doctypes.machine.machine.Machine.validate"
	},
	"Rope Construction": {
		"validate": "maxauto_custom.maxauto.rope_cable.doctypes.rope_construction.rope_construction.RopeConstruction.validate"
	},
	"Bobbin": {
		"validate": "maxauto_custom.maxauto.rope_cable.doctypes.bobbin.bobbin.Bobbin.validate"
	},
	"Stranding Batch": {
		"validate": "maxauto_custom.maxauto.rope_cable.doctypes.stranding_batch.stranding_batch.StrandingBatch.validate",
		"on_submit": "maxauto_custom.maxauto.rope_cable.doctypes.stranding_batch.stranding_batch.StrandingBatch.on_submit"
	},
	"Closing Batch": {
		"validate": "maxauto_custom.maxauto.rope_cable.doctypes.closing_batch.closing_batch.ClosingBatch.validate",
		"on_submit": "maxauto_custom.maxauto.rope_cable.doctypes.closing_batch.closing_batch.ClosingBatch.on_submit"
	},
	"Manufacturing Operation Execution": {
		"validate": "maxauto_custom.maxauto.shopfloor.doctypes.manufacturing_operation_execution.manufacturing_operation_execution.ManufacturingOperationExecution.validate",
		"on_submit": "maxauto_custom.maxauto.shopfloor.doctypes.manufacturing_operation_execution.manufacturing_operation_execution.ManufacturingOperationExecution.on_submit"
	},
	"Unit WIP Transfer": {
		"validate": "maxauto_custom.maxauto.inventory.doctypes.unit_wip_transfer.unit_wip_transfer.UnitWIPTransfer.validate",
		"on_submit": "maxauto_custom.maxauto.inventory.doctypes.unit_wip_transfer.unit_wip_transfer.UnitWIPTransfer.on_submit"
	},
	"Inspection Record": {
		"validate": "maxauto_custom.maxauto.quality.doctypes.inspection_record.inspection_record.InspectionRecord.validate"
	},
	"Packing Record": {
		"validate": "maxauto_custom.maxauto.packing.doctypes.packing_record.packing_record.PackingRecord.validate"
	}
}

# Fixtures to load
fixtures = []

# Desk
# Note: Desk menu items are added via Workspace shortcuts, not hooks