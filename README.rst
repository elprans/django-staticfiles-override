===========================
Django staticfiles override
===========================

:author: Elvis Pranskevichus
:date: 2013/03/25

Staticfiles override allows pattern-based override of static files in Django or
Django modules.  It similar in nature to HTTTP server URL rewrite, but 
functions entirely within Django.


=====
Usage
=====
Staticfiles override configuration is simple.  Add the following to settings.py::

  STATICFILES_OVERRIDES = {
      <URL regular expression>: <replacement> [,
      <URL regular expression>: <replacement>,
      ...
      ]
  }

And then in STATICFILES_FINDERS replace

::

  django.contrib.staticfiles.finders.AppDirectoriesFinder

with

::

  staticfiles_override.finders.AppDirectoriesFinder

Here, "URL regular expression" is any regular expression matching
static file URL, *without* the STATIC_URL prefix and the "replacement"
is the URL of the file that should act as a replacement for the match.  
The replacement may reference match groups within the regular expression.

Example::

  STATICFILES_OVERRIDES = {
     r'^admin/js/jquery(?:\.min)?\.js': r'js/my_\1'
  }

This will override the Django-packaged jquery.js with 
<STATIC_URL>/js/my_jquery.js


Requirements
============

* Python 2.6+
* Django 1.3+
