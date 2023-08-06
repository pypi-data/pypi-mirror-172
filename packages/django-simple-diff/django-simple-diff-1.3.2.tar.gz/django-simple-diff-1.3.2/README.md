# django-simple-diff

Tracks Django model changes before save

## Install

`pip install django-simple-diff`

## Test

```
cd example
PYTHONPATH=".." python3 manage.py test
OR
Install the simple-diff app with `pip install -e <path-to-setup.py>`
```

## Usage

```python
from simple_diff.models import ModelDiffMixin
from django.db import models

class TestDiff(ModelDiffMixin, models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=0)
    test_date = models.DateField(blank=True, null=True)



obj = TestDiff(name='Foo')
obj.name  # 'Foo'

obj.name = 'Bar'
obj.has_changed  # True
obj.changed_fields  # ['name']
obj.get_field_diff('name')  # ('Foo', 'Bar')
```

