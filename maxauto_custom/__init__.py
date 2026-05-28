__version__ = "1.0.0"

# Bridge package for legacy package layout where business modules live under
# the top-level `maxauto` package while Frappe app name is `maxauto_custom`.
import importlib
import sys

_maxauto = importlib.import_module("maxauto")
sys.modules[__name__ + ".maxauto"] = _maxauto
