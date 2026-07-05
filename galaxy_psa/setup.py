from setuptools import find_packages, setup

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="galaxy_psa",
	version="0.0.1",
	description="Galaxy PSA by eKosmos — AI-first Professional Services Automation on Frappe/ERPNext",
	author="eKosmos Inc.",
	author_email="engineering@ekosmos.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
