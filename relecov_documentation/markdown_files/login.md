# Login

The next steps are only for administrators.
Contact the relecov-platform application administrator to provide you with a username and password.

En primer lugar debemos crear un superusuario, que será el administrador (admin).
Esto lo llevaremos a cabo mediante la terminal utilizando el comando: $ python manage.py createsuperuser.
Introduciremos nombre de usuario (Username), dirección de correo electrónico (Email address) y finalmente una contraseña (password).
Tras este paso tendremos definido al administrador de la aplicación relecov-platform.

In the next step, We must navigate to our website, for example http://relecov-platform.isciiides.es then We add /admin at the end of the URL, so
then We will see the next URL: http://relecov-platform.isciiides.es/admin.

Django nos mostrará su panel de administración de la aplicación
imagen

En el panel de la izquierda haremos click sobre Users, en la parte central de la pantalla se desplegará una tabla mostrándonos todos los usuarios registrados en la aplicación, de momento sólo el admininistrador, recién creado en el paso anterior.
Para añadir un nuevo usuario haremos click sobre el botón ADD USER