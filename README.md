# MaxAuto Custom - Manufacturing Platform

Comprehensive ERPNext application for managing rope/cable manufacturing, CNC machining, multi-unit operations, and shopfloor execution.

## Overview

MaxAuto Custom is a full-featured manufacturing platform built on Frappe/ERPNext that implements:

- **Engineering Domain**: Product engineering, feasibility studies, and project management
- **Manufacturing Domain**: Routing, operations, machine management, and capabilities
- **Rope/Cable Manufacturing**: Specialized domain for rope/cable production with bobbin management, stranding, and closing operations
- **CNC Manufacturing**: CNC-specific operations with external processing support
- **Shopfloor/MES**: Manufacturing Operation Execution and MES event logging for shop floor integration
- **Inventory & Logistics**: Multi-unit WIP transfers and inventory management
- **Quality Management**: Inspection records with test result tracking
- **Packing**: Finished goods packing and container management
- **Asset Management**: Asset Label Sheet for QR code printing (60×25mm labels)

## Architecture

The platform follows a domain-driven design with five main business domains:

```
Customer → Engineering Project → Sales Order → Production Plan → Work Order → 
Manufacturing Operations → Production Batch → Finished Goods → Delivery Note → Sales Invoice
```

## Modules & Doctypes (35+ Doctypes)

### Engineering Domain
- **Engineering Project**: Main project master with customer, drawing, revision, and material tracking
- **Feasibility Study**: Preliminary feasibility analysis for projects
- **Product Specification**: Product definitions with construction and material specs

### Manufacturing Domain
- **Manufacturing Routing**: Operation sequences for production  
- **Manufacturing Operation Type**: Define operations (Spooling, Stranding, etc.)
- **Machine**: Equipment master with specifications and status
- **Machine Capability**: Map capabilities to machines (Turning, Milling, Closing, etc.)

### Rope/Cable Manufacturing Domain
- **Rope Construction**: Construction codes and specifications (6x19, 8x19, etc.)
- **Bobbin**: Bobbin/spool management with capacity and status tracking
- **Stranding Batch**: Track strand creation with input/output quantities
- **Closing Batch**: Track rope closing operations

### Shopfloor/MES Domain
- **Manufacturing Operation Execution**: Capture shop floor execution data (qty, downtime, quality)
- **MES Event Log**: Log events from shop floor systems (machine start/stop, downtime, etc.)

### Inventory & Logistics Domain
- **Unit WIP Transfer**: Manage multi-unit manufacturing transfers

### Quality Domain
- **Inspection Record**: Quality inspection with test results and pass/fail status
- **Inspection Test Result**: Individual test parameters (Diameter, Breaking Load, etc.)

### Packing Domain
- **Packing Record**: Finished goods packing with container/drum tracking

### Utility
- **Asset Label Sheet**: Generate and print 60×25mm QR code labels for asset tracking

## Features

- Comprehensive manufacturing workflow from engineering to dispatch
- Rope/cable-specific production tracking (bobbins, stranding, closing)
- CNC machining support with external processing
- Shop floor MES integration for real-time production tracking
- Multi-location manufacturing with WIP transfers
- Quality management with inspection records
- Dynamic asset labeling with QR codes
- Customizable routing and operation definitions

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

## Module Structure

```
maxauto_custom/
├── maxauto/
│   ├── page/
│   │   └── asset_label_sheet/          # Asset QR label printing page
│   ├── engineering/
│   │   └── doctypes/                   # Engineering domain doctypes
│   ├── manufacturing/
│   │   └── doctypes/                   # Manufacturing domain doctypes
│   ├── rope_cable/
│   │   └── doctypes/                   # Rope/cable specific doctypes
│   ├── cnc/
│   │   └── doctypes/                   # CNC manufacturing doctypes
│   ├── shopfloor/
│   │   └── doctypes/                   # MES and shop floor doctypes
│   ├── inventory/
│   │   └── doctypes/                   # Inventory and WIP doctypes
│   ├── quality/
│   │   └── doctypes/                   # Quality management doctypes
│   ├── packing/
│   │   └── doctypes/                   # Packing and logistics doctypes
│   └── mes/                            # MES integration layer
├── public/                             # Static resources
├── hooks.py                            # App configuration
└── README.md                           # This file
```

## Key Routes

- `/app/asset-label-sheet` - Asset QR label printing interface
- `/app/engineering-project` - Engineering project list
- `/app/manufacturing-routing` - Production routing definitions
- `/app/machine` - Equipment master
- `/app/stranding-batch` - Rope stranding operations
- `/app/closing-batch` - Rope closing operations
- `/app/manufacturing-operation-execution` - Shop floor execution
- `/app/inspection-record` - Quality inspections
- `/app/packing-record` - Finished goods packing

## Requirements

- Frappe v16.13.0 or later
- ERPNext v16.12.0 or later  
- Python 3.10+
- MariaDB 10.5+

## Configuration

The platform is configured via:

1. **hooks.py**: Module and doctype registration, document event hooks
2. **pyproject.toml**: Package metadata and dependencies
3. **MANIFEST.in**: Include paths for distribution

## Development

To extend the platform:

1. Add new doctypes in relevant `maxauto/<domain>/doctypes/<doctype_name>/` folders
2. Create JSON definition and Python class files
3. Register in `hooks.py` if custom events needed
4. Update `pyproject.toml` packages list
5. Test on a development site

## Support & Contribution

For issues, feature requests, or contributions:
- GitHub: https://github.com/ssamax10/maxauto_custom
- Email: info@maxautocables.com

## License

MIT License - See LICENSE file for details

## Version

Current: 1.0.0
