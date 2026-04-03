from setuptools import find_packages, setup

setup(
    name="maxauto_custom",
    version="1.0.0",
    description="MaxAuto customizations for ERPNext",
    author="Max Auto Cables Pvt Ltd",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
