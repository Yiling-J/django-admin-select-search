# django-admin-select-search

Add a select box to django admin search.

## Getting Started

This is a django app that add a select box to admin search form.

![alt text](https://dw75asfpu22ml.cloudfront.net/cover/djago_admin_select_example2.jpg)

![alt text](https://dw75asfpu22ml.cloudfront.net/cover/djago_admin_select_example1.png)

```search_fields = ('id', 'title', 'author__full_name')```

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
