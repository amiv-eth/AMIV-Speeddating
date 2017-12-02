# AMIV-Speeddating

Web-Application for the Speeddating Event of the AMIV organized by the AMIV
culture team

## Setup
### Virtualenv
The website runs using flask, and we recommend running it in a virtual
environment. To do this, you first need to initialise it:

	$ virtualenv venv

This will initialise the virtual environment in the `venv` directory. To
activate it, source the following script:

	$ source venv/bin/activate

If that was successful, your `$PS1` should start with `(venv) `.

### Dependencies
Now you need to install the dependencies listed in `requirements.txt`.

	$ pip install -r requirements.txt

### Database & Admin User
To create the database structure and add an admin user, run

	$ ./setup.py <admin_username> <admin_password>

## Run
After that, you can run the website by executing `main.py`. The website is
served at `127.0.0.1:5000` by default.
