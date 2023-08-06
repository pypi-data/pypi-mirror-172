![](https://github.com/django-crispy-forms/crispy-forms-bootstrap2/workflows/crispy-forms-bootstrap2/badge.svg)

# Crispy-forms-boostrap2

Django-crispy-forms bootstrap2 template pack. Until crispy-forms v2 these
templates were included in the core package.

### Install Instructions

Install this plugin using pip:

`pip install crispy-forms-bootstrap2`

Update your project's settings file to add `crispy_forms` and 
`crispy_forms_bootstrap2` to your projects `INSTALLED_APPS`. Also set 
`bootstrap` as and allowed template pack and as the default template pack for 
your project:

```python
INSTALLED_APPS = (
    ...
    "crispy_forms",
    "crispy_forms_bootstrap2",
    ...
)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap"

CRISPY_TEMPLATE_PACK = "bootstrap"
```
