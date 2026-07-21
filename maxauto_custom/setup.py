"""
Setup utilities for the maxauto_custom app.

The `before_install` hook in hooks.py points to `setup_roles` defined here.
This runs before the app's doctypes are synced during `bench install-app`,
ensuring custom Roles referenced in DocType permission rows already exist
so the permission rows are effective immediately after install.
"""

import frappe


# Custom roles used by maxauto DocType permission rows.
# These are NOT standard ERPNext roles, so they must be created on install.
CUSTOM_ROLES = [
    {
        "role_name": "Manufacturing Manager",
        "desk_access": 1,
        "disabled": 0,
        "two_factor": 0,
    },
    {
        "role_name": "Manufacturing User",
        "desk_access": 1,
        "disabled": 0,
        "two_factor": 0,
    },
]


def setup_roles():
    """Create custom roles required by maxauto doctype permissions.

    Idempotent: only creates a role if it does not already exist.
    Safe to run during fresh installs (Helm chart deployments) and
    re-installs.
    """
    for role_def in CUSTOM_ROLES:
        role_name = role_def["role_name"]
        if frappe.db.exists("Role", role_name):
            continue

        role = frappe.get_doc(
            {
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": role_def.get("desk_access", 1),
                "disabled": role_def.get("disabled", 0),
                "two_factor": role_def.get("two_factor", 0),
            }
        )
        role.insert(ignore_permissions=True)
        frappe.logger().info(
            f"maxauto_custom: created Role '{role_name}' during install"
        )

    # Commit so roles are visible to the subsequent migrate step that
    # syncs doctype permission rows.
    frappe.db.commit()