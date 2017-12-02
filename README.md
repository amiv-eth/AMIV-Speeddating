# AMIV-Speeddating

Web-Application for the Speeddating Event of the AMIV organized by the AMIV
culture team

The website runs using flask, and we recommend running it in a virtual
environment. To do this, you first need to initialise it:

	$ virtualenv venv

This will initialise the virtual environment in the `venv` directory. To
activate it, source the following script:

	$ source venv/bin/activate

If that was successful, your `$PS1` should start with `(venv) `. Now you
need to install the dependencies listed in `requiremts.txt`.

	$ pip install -r requirements.txt

After that, you can run the website by executing `main.py`. The website is
served at `127.0.0.1:5000` by default.

## Add admin user
To add an admin user, you must create an `AdminUser` instance. To add user `adminuser` with password `adminpassword` use the following

	from app.models import AdminUser
	from app import db, bcrypt

	u = AdminUser()
	u.username = 'adminuser'
	u.password = bcrypt.generate_password_hash('adminpassword')

	db.session.add(u)
	db.session.commit()
