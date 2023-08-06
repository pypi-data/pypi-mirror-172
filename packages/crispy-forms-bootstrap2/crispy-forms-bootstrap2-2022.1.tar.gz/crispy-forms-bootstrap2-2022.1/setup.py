from setuptools import find_packages, setup

setup(
    name="crispy-forms-bootstrap2",
    version="2022.1",
    packages=find_packages(),
    url="https://github.com/django-crispy-forms/crispy-forms-bootstrap2",
    license="MIT",
    description="Django-crispy-forms bootstrap2 templates",
    install_requires=["django-crispy-forms >= 1.8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
    ],
    include_package_data=True,
    zip_safe=False,
)
