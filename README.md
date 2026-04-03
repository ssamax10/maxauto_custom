# MaxAuto Custom

Custom ERPNext app for Max Auto Cables.

## Features

- Asset Label Sheet page for printing 60x25 mm asset QR labels
- Works from ERPNext Assets workspace
- Select, filter, and print selected assets

## Route

- /app/asset-label-sheet

## Installation on another bench

1. Get the app into bench:
   bench get-app https://github.com/ssamax10/maxauto_custom.git
2. Install on target site:
   bench --site <site_name> install-app maxauto_custom
3. Run migrations:
   bench --site <site_name> migrate

## Notes

- Requires Frappe/ERPNext v16.
- The workspace link to Asset Label Sheet is expected in the Assets workspace.
