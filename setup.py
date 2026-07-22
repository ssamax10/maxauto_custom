from pathlib import Path
import re
from setuptools import find_packages, setup


def read_version():
    version_file = Path(__file__).parent / "maxauto_custom" / "_version.py"
    content = version_file.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', content, re.M)
    if not match:
        raise RuntimeError("Unable to find __version__ in maxauto_custom/_version.py")
    return match.group(1)

packages = find_packages(include=[
    "maxauto_custom",
    "maxauto_custom.*",
    "maxauto",
    "maxauto.*",
    "commands",
    "commands.*",
])

setup(
    name="maxauto_custom",
    version=read_version(),
    description="MaxAuto customizations for ERPNext",
    author="Max Auto Cables Pvt Ltd",
    packages=packages,
    include_package_data=True,
    package_data={
        "maxauto_custom": ["hooks.py", "modules.txt"],
    },
    zip_safe=False,
)
