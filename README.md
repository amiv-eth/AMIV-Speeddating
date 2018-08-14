# AMIV-Speeddating

Web-Application for the Speeddating Event of the AMIV organized by the AMIV
culture team

## Development

### Virtualenv

The website runs using flask, and we recommend running it in a virtual
environment. To do this, you first need to initialize it:

```bash
virtualenv venv
```

This will initialise the virtual environment in the `venv` directory. To
activate it, source the following script:

```bash
source venv/bin/activate
```

If that was successful, your `$PS1` should start with `(venv) `.

### Dependencies

Now you need to install the dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Database & Admin User

To create the database structure and add an admin user, run

```bash
./setup.py <admin_username> <admin_password>
```

### Run
After that, you can run the website by executing `main.py`. The website is
served at `127.0.0.1:5000` by default.

## Deploy
The AMIV-Speeddating website is available as a [docker](https://www.docker.com) container.
You need an external MySQL database.

Next, create a configuration based on `app/example-config.py` and save it (as a docker config).

Finally, create the speeddating website service and mount the configuration file to `/speeddating/app/config.py`.

*Please note that the service is available on port `8080`!*
