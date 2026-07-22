"""Compatibility hooks file for source-checkout development.

Keep the canonical hooks in the installable package at
`maxauto_custom/hooks.py` so packaged deployments (Docker/Helm/K3s)
and local bench development use the same hook definitions.
"""

from maxauto_custom.hooks import *  # noqa: F403