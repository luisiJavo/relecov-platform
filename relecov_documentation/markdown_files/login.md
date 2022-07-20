# Login

<red>The next steps are only for administrators.</red>


Contact the relecov-platform application administrator to provide you with a username and password.

First of all we must create a superuser, which will be the administrator (admin).
We will do this through the terminal using the command:

 `$ python manage.py createsuperuser`

We will enter username (Username), email address (Email address) and finally a password (password).
After this step we will have defined the administrator of the relecov-platform application.

In the next step, We must navigate to our website, for example http://relecov-platform.isciiides.es then We add /admin at the end of the URL, so
then We will see the next URL: http://relecov-platform.isciiides.es/admin.

Django will show us the administration panel of the application

![relecov-platform admin main page](./relecov-platform/relecov_documentation/img/admin_panel_main.png)

In the left panel we will click on Users

![relecov-platform admin add user 1](./relecov_documentation/img/admin_panel_add_user1.png)


In the central part of the screen, a table will be displayed showing us all the users registered in the application, at the moment only the administrator, recently created in the previous step.
To add a new user we will click on the ADD USER button.

![relecov-platform admin add user 2](./relecov_documentation/img/admin_panel_add_user2.png)

![relecov-platform admin add user 3](./relecov_documentation/img/admin_panel_add_user3.png)