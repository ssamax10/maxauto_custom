# MaxAuto Custom - Manufacturing Platform

Comprehensive ERPNext application for managing rope/cable manufacturing, CNC machining, multi-unit operations, and shopfloor execution.

## Overview

MaxAuto Custom is a full-featured manufacturing platform built on Frappe/ERPNext that implements:

- **Plant Management**: Multi-plant operations with warehouse and cost center configuration
- **Engineering Domain**: Product engineering, feasibility studies, and project management
- **Manufacturing Domain**: Routing, operations, machine management, and capabilities
- **Material Management**: Material specifications with chemical composition and certification tracking
- **Rope/Cable Manufacturing**: Specialized domain for rope/cable production with bobbin management, stranding, and closing operations
- **CNC Manufacturing**: CNC-specific operations with external processing support
- **Shopfloor/MES**: Manufacturing Operation Execution and MES event logging for shop floor integration
- **Inventory & Logistics**: Multi-unit WIP transfers with automatic stock entry creation
- **Quality Management**: Inspection records with test result tracking and supplier approval workflow
- **Packing**: Finished goods packing with automatic stock movement
- **Asset Management**: Asset Label Sheet for QR code printing (60×25mm labels)

## Architecture

The platform follows a domain-driven design with a single module (`Maxauto`) organized into logical subfolders:

```
Customer → Engineering Project → Sales Order → Production Plan → Work Order → 
Manufacturing Operations → Production Batch → Finished Goods → Delivery Note → Sales Invoice
```

## Module Structure

```
maxauto_custom/
├── maxauto/                          # Single module (Maxauto)
│   ├── plant/                        # Plant Management
│   │   └── doctype/
│   │       └── plant/                # Plant master with warehouses & contacts
│   │
│   ├── engineering/                  # Engineering Domain
│   │   └── doctype/
│   │       ├── engineering_project/
│   │       ├── feasibility_study/
│   │       └── product_specification/
│   │
│   ├── manufacturing/                # Manufacturing Domain
│   │   └── doctype/
│   │       ├── manufacturing_routing/
│   │       ├── manufacturing_operation_type/
│   │       ├── manufacturing_operation_execution/
│   │       ├── machine/
│   │       └── machine_capability/
│   │
│   ├── material/                     # Material Management
│   │   └── doctype/
│   │       └── material_specification/  # Material specs with composition
│   │
│   ├── rope_cable/                   # Rope/Cable Manufacturing
│   │   └── doctype/
│   │       ├── rope_construction/
│   │       ├── bobbin/
│   │       ├── stranding_batch/
│   │       └── closing_batch/
│   │
│   ├── cnc/                          # CNC Manufacturing
│   │   └── doctype/
│   │
│   ├── quality/                      # Quality Management
│   │   └── doctype/
│   │       ├── inspection_record/
│   │       ├── inspection_test_result/
│   │       └── supplier_approval/    # Supplier approval workflow
│   │
│   ├── inventory/                    # Inventory & Logistics
│   │   └── doctype/
│   │       └── unit_wip_transfer/    # Creates Stock Entry on submit
│   │
│   ├── packing/                      # Packing
│   │   └── doctype/
│   │       └── packing_record/       # Creates Stock Entry on submit
│   │
│   ├── shopfloor/                    # Shopfloor
│   │   └── doctype/
│   │
│   ├── mes/                          # MES Integration
│   │   └── doctype/
│   │       └── mes_event_log/
│   │
│   ├── purchasing/                   # Purchasing (placeholder)
│   │   └── doctype/
│   │
│   ├── report/                       # Script Reports
│   │   └── report/
│   │
│   ├── print_format/                 # Print Formats
│   │   └── print_format/
│   │
│   ├── workflow/                     # Workflows
│   │   └── workflow/
│   │
│   └── page/                         # Custom Pages
│       └── asset_label_sheet/
│
├── fixtures/                         # Version-controlled customizations
│   ├── workspace.json
│   ├── custom_field.json
│   ├── property_setter.json
│   ├── client_script.json
│   ├── server_script.json
│   ├── print_format.json
│   ├── workflow.json
│   └── notification.json
│
├── public/                           # Static resources
│   ├── css/
│   └── js/
│
├── templates/                        # Jinja templates
│   └── includes/
│
├── hooks.py                          # App configuration
├── modules.txt                       # Module registration
├── pyproject.toml                    # Package metadata
└── README.md                         # This file
```

## DocTypes (40+ Doctypes)

### Plant Management
- **Plant**: Manufacturing facility master with default warehouses, cost center, and contact information

### Engineering Domain
- **Engineering Project**: Main project master with customer, drawing, revision, and material tracking
- **Feasibility Study**: Preliminary feasibility analysis for projects
- **Product Specification**: Product definitions with construction and material specs

### Manufacturing Domain
- **Manufacturing Routing**: Operation sequences for production  
- **Manufacturing Operation Type**: Define operations (Spooling, Stranding, etc.)
- **Machine**: Equipment master with specifications and status
- **Machine Capability**: Map capabilities to machines (Turning, Milling, Closing, etc.)

### Material Management
- **Material Specification**: Material specs with chemical composition, mechanical properties, dimensions, and certification requirements

### Rope/Cable Manufacturing Domain
- **Rope Construction**: Construction codes and specifications (6x19, 8x19, etc.)
- **Bobbin**: Bobbin/spool management with capacity and status tracking
- **Stranding Batch**: Track strand creation with input/output quantities
- **Closing Batch**: Track rope closing operations

### Shopfloor/MES Domain
- **Manufacturing Operation Execution**: Capture shop floor execution data (qty, downtime, quality)
- **MES Event Log**: Log events from shop floor systems (machine start/stop, downtime, etc.)

### Inventory & Logistics Domain
- **Unit WIP Transfer**: Manage multi-unit manufacturing transfers (creates Stock Entry on submit)

### Quality Domain
- **Inspection Record**: Quality inspection with test results and pass/fail status
- **Inspection Test Result**: Individual test parameters (Diameter, Breaking Load, etc.)
- **Supplier Approval**: Supplier quality approval workflow with audit tracking

### Packing Domain
- **Packing Record**: Finished goods packing with container/drum tracking (creates Stock Entry on submit)

### Utility
- **Asset Label Sheet**: Generate and print 60×25mm QR code labels for asset tracking

## Features

- Comprehensive manufacturing workflow from engineering to dispatch
- Multi-plant support with plant-specific warehouses and cost centers
- Rope/cable-specific production tracking (bobbins, stranding, closing)
- CNC machining support with external processing
- Shop floor MES integration for real-time production tracking
- Multi-location manufacturing with WIP transfers
- Quality management with inspection records
- Supplier approval workflow with audit tracking
- Material specification management with chemical composition
- Dynamic asset labeling with QR codes
- Customizable routing and operation definitions
- Automatic stock entry creation for WIP transfers and packing
- Version-controlled fixtures for customizations

## Fixtures

The app uses fixtures to version-control customizations:

```bash
# Export all fixtures
bench --site <site> export-fixtures --app maxauto_custom

# Export specific doctype
bench --site <site> export-fixtures --app maxauto_custom --doctype "Print Format"
```

Fixtures include:
- Workspace
- Custom Fields
- Property Setters
- Client Scripts
- Server Scripts
- Print Formats
- Workflows
- Workflow States
- Notifications

## Installation

### On a new bench:

```bash
bench get-app https://github.com/ssamax10/maxauto_custom.git
bench --site <site_name> install-app maxauto_custom
bench --site <site_name> migrate
```

### On existing bench:

```bash
cd frappe-bench
bench get-app https://github.com/ssamax10/maxauto_custom.git
bench --site <site_name> install-app maxauto_custom
```

## Key Routes

- `/app/plant` - Plant master
- `/app/material-specification` - Material specifications
- `/app/supplier-approval` - Supplier approval workflow
- `/app/asset-label-sheet` - Asset QR label printing interface
- `/app/engineering-project` - Engineering project list
- `/app/manufacturing-routing` - Production routing definitions
- `/app/machine` - Equipment master
- `/app/stranding-batch` - Rope stranding operations
- `/app/closing-batch` - Rope closing operations
- `/app/manufacturing-operation-execution` - Shop floor execution
- `/app/inspection-record` - Quality inspections
- `/app/packing-record` - Finished goods packing
- `/app/unit-wip-transfer` - WIP transfers

## Requirements

- Frappe v16.13.0 or later
- ERPNext v16.12.0 or later  
- Python 3.10+
- MariaDB 10.5+

## Configuration

The platform is configured via:

1. **hooks.py**: Module and doctype registration, document event hooks, fixtures
2. **pyproject.toml**: Package metadata and dependencies
3. **MANIFEST.in**: Include paths for distribution

## Development

To extend the platform:

1. Add new doctypes in relevant `maxauto/<domain>/doctypes/<doctype_name>/` folders
2. Create JSON definition and Python class files
3. Register in `hooks.py` if custom events needed
4. Update `pyproject.toml` packages list
5. Test on a development site
6. Export fixtures for version control

### Local Development Setup

```bash
# Start infrastructure
docker-compose up -d

# Initialize bench (first time)
python installer.py --apps-json apps-example.json --site-name test.localhost --admin-password admin

# Start development server
cd frappe-bench
bench start

# Access at: http://test.localhost:8000
# Login: Administrator / admin
```

### Common Commands

```bash
# Run migrations
bench --site test.localhost migrate

# Clear cache
bench --site test.localhost clear-cache

# Rebuild assets
bench build --app maxauto_custom

# Export fixtures
bench --site test.localhost export-fixtures --app maxauto_custom

# Run tests
bench --site test.localhost run-tests --app maxauto_custom
```

## Support & Contribution

For issues, feature requests, or contributions:
- GitHub: https://github.com/ssamax10/maxauto_custom
- Email: info@maxautocables.com

## License

MIT License - See LICENSE file for details

## Version

Current: 1.1.1

### Changelog

**v1.1.0**
- Added Plant DocType for multi-plant operations
- Added Material Specification DocType
- Added Supplier Approval DocType with workflow
- Fixed Unit WIP Transfer to create and submit Stock Entry
- Implemented Packing Record stock entry creation
- Added fixtures configuration for version-controlled customizations
- Reorganized folder structure for scalability

**v1.0.0**
- Initial release with manufacturing, quality, and MES doctypes