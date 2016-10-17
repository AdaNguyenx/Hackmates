HackerPack | Project Docs
=================================

# Table of Contents
### **[Initial Setup](#initial-setup)**

### **[Explanation of which does what](#explanation-of-which-does-what)**

- **[HaPa/HackerPack](#hapa-1)**

    - **[HaPa/HackerPack/HackerPack](#hapa-2)**
        - **[forms.py](#forms)**
        - **[settings.py](#settings)**
        - **[urls.py](#urls)**

    - **[HaPa/HackerPack/src](#src)**
        - **[models.py](#models)**
        - **[urls.py](#src-urls)**
        - **[views.py](#views)**

    - **[HaPa/HackerPack/static](#static)**

    - **[HaPa/HackerPack/templates](#templates)**

### **[Process of Adding A New HTML Page](#newpage)**
### **[Understanding Our Forms](#ourforms)**
### **[Helpful resources](#helpful-resources)**

---------------------------------
# Initial Setup
-------------------

###Requirements###
- Python 2.7
- Postgres
- npm

###Initial Setup###

Setting up Virtual Environment, *should be created at the highest project directory level*

```
virtualenv .env
source .env/bin/activate

pip install -r requirements.txt
```

###Creating Database in Postgres###
```
createdb hapa
```

###Installing SCSS Transpiler
---------
You need to have npm installed, which can be done if you brew by:
```
brew install node
```

Installing the packages required is done by:

```
sudo npm install gulp -g
npm install
```

The first installation installs the gulp CLI for using gulp's compilers/compressors/transpilers

Secondly, the npm install installs all the dependant packages required for our script

---------

To start Gulp you must type in:

```
gulp
```

###Starting Project###
*Make sure you've activated the correct python environment*
Run two terminals (Cmd + T on your terminal application)

Terminal one
```
python HackerPack/manage.py migrate
python HackerPack/manage.py runserver
```

Terminal two
```
gulp
```

Creating a super user to enter facebook api information
```
python HackerPack/manage.py createsuperuser
```

Login through the admin panel at: `http://127.0.0.1:8000/admin`

Click on `Add Social Application`

Enter the bottom information:

Client ID: `1562330974062551`

Client Key: `42097228407e213d3918e0f95336c9ff`

Add Site through the `+` button where the url is:`http://127.0.0.1:8000`  and the sitename is `HackerPack`


###See online###

http://127.0.0.1:8000





###Errors###
If error django.db.utils.OperationalError: FATAL:  role "jaime5" does not exist shows do:

createuser jaime5

---------------------------------
# Explanation of which does what
-------------------
## HaPa/HackerPack <a id="hapa-1"></a>
This is where Django works, everything outside this folder is misc stuff.

### HaPa/HackerPack/HackerPack <a id="hapa-2"></a>
This is where the master configurations for everything in the app is located

- #### forms.py <a id="forms"></a>
Custom signup form for users.

- #### settings.py <a id="settings"></a>
Settings for the whole project. If there are things in there that are not explained below, they are most likely code
for production or default Django code that you can ignore.
    - INSTALLED_APPS: add new app you create under `# Personal Apps` and third-party applications under `# Remote Packages`
    - ROOT_URLCONF: where the main urls.py file is located
    - TEMPLATES: the folder where the HTML templates are located
    - STATICFILES_DIRS: the folder where all the static files (images, css, etc.) are located.
    It is where where Django will look into when you do `{% load staticfiles %}`

- #### */HackerPack/urls.py <a id="urls"></a>
Where you connect the path of the Django app with the function in */src/views.py that renders that path.
For example, in this file, you can specify that hackerpack.io/login will be rendered by file login.html. See
[Process of Adding A New HTML Page](#newpage) for further reference.

### HaPa/HackerPack/src <a id="src"></a>
The Django app that controls anything that happens with the main page app.

- #### models.py <a id="models"></a>
- A model is similar to a database table. It has several fields which are similar to database columns.
You can create a new model/schema for any data type you want to use.
- ** How to create a new model: **


```python
# Importing necessary packages
from django.contrib import admin
from django.db import models

# Create a new model/schema
class DummyData(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()

# Give permissions for admin to change DummyData
admin.site.register(DummyData)
```

- If you make any changes to models.py, you need to perform these two commands

```
python HackerPack/manage.py makemigrations
python HackerPack/managepy migrate
```


- #### */src/urls.py <a id="src-urls"></a>
The urls for "src" app.

- #### views.py <a id="views"></a>
Where you write functions on that control rendering HTML pages and sending and receiving data from users.
See [Process of Adding A New HTML Page](#newpage) for further reference.


### HaPa/HackerPack/static <a id="static"></a>
The folder where all the static files (css, images, videos, etc.) are stored.

### HaPa/HackerPack/templates<a id="templates"></a>
The folder where all the HTML templates that are rendered through */src/views.py are stored.

---------------------------------
# Process of Adding A New HTML Page <a id="newpage"></a>
-------------------
Django requires at minimum two things to serve a page in addition to the HTML document:

 * A function that renders the page
 * A regex that addresses a direction for a page



### Inside */views.py

```python
def newFunction(request):
    context = {
    'A_KEYWORD': A_VARIABLE_OR_OBJECT,
    }

    return render(request, 'HTML_FILE', context)
```
The `newFunction` serves a simple "GET" request, which then renders the HTML file named: `'HTML_FILE'`

Data can then be transferred to the HTML file by adding `{{ A_KEYWORD }}` to the HTML file

The `A_KEYWORD` then sends whatever is assigned to `A_VARIABLE_OR_OBJECT` in the dictionary


### Inside */urls.py
```python
...
from . import views
...

urlpatterns = [
    ...
    url(r'^world/isNew/$', views.newFuncton, name='newFunction'),
]
```
First we imported our previously defined function `newFunction(request)`from views.py

Secondly, we have assigned a regex so that the specified address would serve the page:`http://localhost:8000/world/isNew`

Finally, we have assigned a namespace to our new URL named: `newFunction`

---------------------------------
# Understanding our forms <a id="ourforms"></a>
-------------------
Custom Form
```python
from django import forms

class SettingsForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Change first name')
    last_name = forms.CharField(max_length=30, label='Change last name')

    def update(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
```
Location inside */views.py
```python
...
def somePageWithAFormView(request):
    if request.method == 'POST':
        form = forms.SettingsForm(request.POST)
        if form.is_valid():
            user = request.user
            form.update(request, user)
            HttpResponseRedirect('/accounts/profile')
    else:
        settingForm = forms.SettingsForm()
        context = {
            'title': 'My Profile',
            'form': settingForm
        }
        return render(request, 'account/profile.html', context)
```
Case 1: Default Form
 * When a user first visits this page with this form the default `request.method = "GET"`
 * Django then generates a form using the inputs defined in Custom Form
 * Since nothing is passed into settingsForm() a clean form is rendered for the user to input data

Case 2: When They Submit
 * When a user enters data into the form and submits the form, then the `request.method = "POST"`
 * The user's inputted data is then passed into the form
 * The function `form.is_valid()` checks to see whether or not the information inputted is valid
 * Our `form.update` function manages updating the new user inputted information to the database
 * Finally, our user is redirected to a new page using `HttpResponseRedirect('YOUR_URL')`

---------------------------------
# Helpful Resources
-------------------
- [Django Allauth](http://stackoverflow.com/questions/20632061/override-django-allauth-default-forms)
- [All Auth Tutorial](http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/)
