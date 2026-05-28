from setuptools import find_packages, setup

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
    version="1.0.0",
    description="MaxAuto customizations for ERPNext",
    author="Max Auto Cables Pvt Ltd",
    packages=packages,
    include_package_data=True,
    zip_safe=False,
)
