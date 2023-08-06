=============================
sssauth
=============================

sssauth is a pluggable Django app that enables login/signup via an SSS Extension.


Example project
---------------

https://github.com/SafelySignSymbol/django-sss-auth-boilerplate/tree/master/example

You can check out our example project by cloning the repo and heading into example/ directory.
There is a README file for you to check, also.


Features
--------

* Web3 API login, signup
* Web3 Django forms for signup, login
* Checks ethereum address validity
* Uses random token signing as proof of private key posession
* Easy to set up and use (just one click)
* Custom auth backend
* VERY customizable - uses Django settings, allows for custom User model
* Vanilla Javascript helpers included

Install
----------
Install sssuth with pip::

    pip install sssauth


Credits
-------

Tools used in rendering this package:

*  `Django-web3-auth`: https://github.com/Bearle/django-web3-auth
*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage