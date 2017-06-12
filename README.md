# django-admin-select-search

Add a select box to django admin search.

## Getting Started

This is a django app that add a select box to admin search form.

### Prerequisites

django 1.10


### Installing

This is nothing but a django app. So just copy searchadmin to your project folder,
add to your install apps, then use it instead of old django admin.


```
from searchadmin.admin import SelectModelAdmin

class NewAdmin(SelectModelAdmin)
	pass

```
