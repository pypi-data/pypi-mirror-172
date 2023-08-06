======
awsgi2
======


AWSGI allows you to use WSGI-compatible middleware and frameworks like Flask and Django with the `AWS API Gateway/Lambda proxy integration <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html>`_.

This is an improved fork of `original aws-wsgi <https://github.com/slank/awsgi>`_.

Installation
------------

``awsgi2`` is available from PyPI as ``awsgi2``::

    pip install awsgi2

Examples
--------

Flask
^^^^^

.. code-block:: python

    import awsgi2
    from flask import (
        Flask,
        jsonify,
    )

    app = Flask(__name__)


    @app.route('/')
    def index():
        return jsonify(status=200, message='OK')


    def lambda_handler(event, context):
        return awsgi2.response(app, event, context, base64_content_types={"image/png"})

Django
^^^^^^

.. code-block:: python

    import os
    import awsgi2

    from django.core.wsgi import get_wsgi_application

    # my_app_directory/settings.py is a vanilla Django settings file, created by "django-admin startproject".
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_app_directory.settings')
    # In the settings.py file, you may find it useful to include this setting to remove
    # Django's need for SQLite, which is currently (2020-11-17) outdated in the Lambda runtime image
    # DATABASES = { 'default': { 'ENGINE': 'django.db.backends.dummy', } }

    application = get_wsgi_application()

    def lambda_handler(event, context):
        return awsgi2.response(application, event, context, base64_content_types={"image/png"})


Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it::

    docker build --ssh default --target devel_shell -t awsgi2:devel_shell .
    docker create --name awsgi2_devel -v `pwd`":/app" -it `echo $DOCKER_SSHAGENT` awsgi2:devel_shell
    docker start -i awsgi2_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i awsgi2_devel /bin/bash -c "pre-commit install"
    docker exec -i awsgi2_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run --rm -it -v `pwd`":/app" awsgi2:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t awsgi2:tox .
    docker run --rm -it -v `pwd`":/app" `echo $DOCKER_SSHAGENT` awsgi2:tox

Development
-----------

TLDR:

- Create and activate a Python 3.8 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.8` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go.

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).
