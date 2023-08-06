# django-cloudspotlicense
Django package to integrate the authentication of the Cloudspot License Server in other django applications.


## Getting started

### Install

Install with pip.

```python
pip install django-cloudspotlicense
```

### Quick start

1. Add ```django_cloudspotlicense``` to your INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'django_cloudspotlicense'
]
```

2. Include the URLConf in your project urls.py

```python
urlpatterns = [
    path('auth/', include('django_cloudspotlicense.urls')),
]
```

3. Run ``python manage.py migrate`` to create all the required models

4. Use the ```LoginView``` to let users log in using the Cloudspot License Server

```python
import django_cloudspotlicense.views as auth_views

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login')
]
```

A basic html template with no styling will be provided. You can overwrite this template by simply creating a new template at ```templates/auth/login.html```.
The only requirement for this template is that it includes two input elements with the name ```username``` and ```password```.

```html
<input type="text" name="username" />
<input type="password" name="password" />
```

5. Done

## Setting up the User model

You can extend the User model as usual to add more attributes. ```django_cloudspotlicense``` also uses the User model to store additional information, such as tokens and the company id.
If you want to add additional attributes, import the User class from the package and add your attributes as usual.

```python
from django_cloudspotlicense.models import CloudspotUser

class User(CloudspotUser):
    extra_data = models.CharField(max_length=500, default='foobar')
```

Use as normal.

```python
print(user.extra_data) # foobar
```

## Webhook

This package also provides a webhook where the Cloudspot License Server will send updates to whenever the permissions for a user changes.
The webhook is located at ```https://example.com/auth/webhook```. This webhook is automatically activated when importing the URLConf.