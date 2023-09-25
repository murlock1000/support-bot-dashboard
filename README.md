# [Django Material Dashboard](https://appseed.us/product/material-dashboard/django/)

Open-source **Django** project crafted on top of **[Material Dashboard](https://appseed.us/product/material-dashboard/django/)**, an open-source `Boostrap 5` design from [Creative-Tim](https://www.creative-tim.com/?AFFILIATE=128200)
The product is designed to deliver the best possible user experience with highly customizable feature-rich pages. `Material Material` has easy and intuitive responsive design whether it is viewed on retina screens or laptops.

- 👉 [Django Material Dashboard](https://appseed.us/product/material-dashboard/django/) - `Product page`
- 👉 [Django Material Dashboard](https://django-material-dash2.onrender.com) - `LIVE Demo`
- 🛒 **[Django Material Dashboard PRO](https://appseed.us/product/material-dashboard2-pro/django/)** - `Premium Version`

<br />

> Features: 

- ✅ `Up-to-date Dependencies`
- ✅ Theme: [Django Admin Material](https://github.com/app-generator/django-admin-material-dashboard), **designed by [Creative-Tim](https://www.creative-tim.com/product/material-dashboard?AFFILIATE=128200)**
  - `can be used in any Django project` (new or legacy)
- ✅ **Authentication**: `Django.contrib.AUTH`, Registration
- Support-bot ticket metadata display
  - ❌ Open/Closed ticket count
  - ❌ Average open ticket time
  - ❌ Completed ticket count per date range and tags
- Staff analytics per staff
  - ❌ Open/Closed tickets
  - ❌ Closed ticket count per date range and tags
- Single ticket analysis
  - ❌ Display ticket metadata (raised by, claimed by, name...)
  - ❌ Display ticket tags
  - ❌ Retrieve and display ticket messages (admin only)
    - ❌ Text messages
    - ❌ Images
    - ❌ Reactions
    - ❌ Replies
    - ❌ Other messages (calls)
- Single ticket commands
  - ❌ Add/Modify ticket tags
  - ❌ Close/Reopen ticket
  - ❌ Assign staff to ticket
- Support-bot commands
  - ❌ Give staff status for user
  - ❌ Raise ticket for user and staff
  - ❌ Create custom tag
<br />

## Manual Build 

> 👉 Download the code  

```bash
$ git clone https://github.com/murlock1000/support-bot-dashboard.git
$ cd support-bot-dashboard
```

<br />
> 👉 Initialize/update sub-modules  

```bash
$ git submodule update --init --recursive
$ git submodule update --recursive --remote
```

> 👉 Install packages via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r ./support_bot/requirements.txt
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database (for web-interface)

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- home/
   |    |-- views.py                     # APP Views 
   |    |-- urls.py                      # APP Routing
   |    |-- models.py                    # APP Models 
   |    |-- tests.py                     # Tests  
   |    |-- templates/                   # Theme Customisation 
   |         |-- includes                # 
   |              |-- custom-footer.py   # Custom Footer      
   |     
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## How to Customize 

When a template file is loaded, `Django` scans all template directories starting from the ones defined by the user, and returns the first match or an error in case the template is not found. 
The theme used to style this starter provides the following files: 

```bash
# This exists in ENV: LIB/admin_material
< UI_LIBRARY_ROOT >                      
   |
   |-- templates/                     # Root Templates Folder 
   |    |          
   |    |-- accounts/       
   |    |    |-- login.html           # Sign IN Page
   |    |    |-- register.html        # Sign UP Page
   |    |
   |    |-- includes/       
   |    |    |-- footer.html          # Footer component
   |    |    |-- sidebar.html         # Sidebar component
   |    |    |-- navigation.html      # Navigation Bar
   |    |    |-- scripts.html         # Scripts Component
   |    |
   |    |-- layouts/       
   |    |    |-- base.html            # Masterpage
   |    |    |-- base-auth.html       # Masterpage for Auth Pages
   |    |
   |    |-- pages/       
   |         |-- index.html           # Dashboard Page
   |         |-- profile.html         # Profile Page
   |         |-- *.html               # All other pages
   |    
   |-- ************************************************************************
```

When the project requires customization, we need to copy the original file that needs an update (from the virtual environment) and place it in the template folder using the same path. 

> For instance, if we want to **customize the footer.html** these are the steps:

- ✅ `Step 1`: create the `templates` DIRECTORY inside the `home` app
- ✅ `Step 2`: configure the project to use this new template directory
  - `core/settings.py` TEMPLATES section
- ✅ `Step 3`: copy the `footer.html` from the original location (inside your ENV) and save it to the `home/templates` DIR
  - Source PATH: `<YOUR_ENV>/LIB/admin_material/template/includes/footer.html`
  - Destination PATH: `<PROJECT_ROOT>home/templates/includes/footer.html`

> To speed up all these steps, the **codebase is already configured** (`Steps 1, and 2`) and a `custom footer` can be found at this location:

`home/templates/includes/custom_footer.html` 

By default, this file is unused because the `theme` expects `footer.html` (without the `custom-` prefix). 

In order to use it, simply rename it to `footer.html`. Like this, the default version shipped in the library is ignored by Django. 

In a similar way, all other files and components can be customized easily.

<br />

## CSS Styling 

The UI can be customized via the SCSS file. This setup was tested using: 

- `Node` v16.15.0
- `Yarn` 1.22.18 
- `Gulp` CLI version: `2.3.0`, Local version: `4.0.2`

```bash
$ cd static
$ yarn                                       # Install Modules 
$ vi scss/material-dashboard/_variables.scss # Edit primary, secondary colors
$ gulp                                       # Regenerate CSS files   
```

> NOTE, once the CSS files are successfully regenerated, force a hard refresh in the browser (Shift + F5 in Chrome).

The relevant lines in `_variables.scss` are highlighted below: 

```SCSS
// _variables.scss, LINES 56 -> 63
$primary:       #e91e63 !default;   // EDIT & Recompile SCSS
$secondary:     #7b809a !default;   // EDIT & Recompile SCSS
$info:          #1A73E8 !default;   // EDIT & Recompile SCSS
$success:       #4CAF50 !default;   // EDIT & Recompile SCSS
$warning:       #fb8c00 !default;   // EDIT & Recompile SCSS
$danger:        #F44335 !default;   // EDIT & Recompile SCSS
$light:         $gray-200 !default; // EDIT & Recompile SCSS
$dark:          $h-color !default;  // EDIT & Recompile SCSS
```
<br />