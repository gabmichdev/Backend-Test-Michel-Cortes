#!/usr/bin/env bash

cd /opt/cornershop/backend-test

# image can run in multiple modes
if [[ "${1}" == "shell" ]]; then
    exec /bin/bash
elif [[ "${1}" == "migrate-noinput" ]]; then
    exec python manage.py migrate --noinput
elif [[ "${1}" == "collectstatic" ]]; then
    exec python manage.py collectstatic --noinput
elif [[ "${1}" == "jupyterlab" ]]; then
    dev pipi jupyterlab==1.2.6 nbresuse==0.3.3
    # install audited-notebook if we need auditing
    # this installs over the notebook package from the previous dev pipi
    # there is really no good avoid installing twice due to the different package name (audited-notebook vs notebook)
    if [[ "${JUPYTER_AUDIT}" == "true" ]]; then
        # https://github.com/gclen/audited-notebook
        dev pipi https://github.com/gclen/audited-notebook/archive/6.0.1_pypi_with_mods.zip
        sed -i 's/%(asctime)s %(hostname)s AUDIT_LOG: Date: %(date)s User: %(user)s Code: %(message)s/%(asctime)s AUDIT: %(message)s/g' ~/.local/lib/python3.7/site-packages/notebook/services/kernels/kernel_logging_conf.py
    fi

    mkdir -p /opt/cornershop/.local/share/jupyter/kernels/django 2>/dev/null
    echo "{\"interrupt_mode\": \"signal\", \"display_name\": \"Django\", \"env\": {}, \"language\": \"python\", \"argv\": [\"python\", \"-m\", \"ipykernel_launcher\", \"-f\", \"{connection_file}\", \"--ext\", \"django_extensions.management.notebook_extension\"], \"metadata\": {}}" > /opt/cornershop/.local/share/jupyter/kernels/django/kernel.json

    mkdir ~/.jupyter 2>/dev/null
    jupyter serverextension enable --py nbresuse
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.port = 8000" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.token=''" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.password=''" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.NotebookApp.terminals_enabled = False" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.KernelSpecManager.whitelist = {'django'}" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.MappingKernelManager.cull_idle_timeout = 900" >> ~/.jupyter/jupyter_notebook_config.py
    echo "c.InteractiveShellApp.extensions = ['django_extensions.management.notebook_extension']" >> ~/.jupyter/jupyter_notebook_config.py

    exec jupyter lab

elif [[ "${1}" == "celery" ]]; then
    APP="${APP:-backend_test}"
    QUEUES="${QUEUES:-celery}"
    LOG_LEVEL="${LOG_LEVEL:-info}"
    CONCURRENCY="${CONCURRENCY:-1}"
    MAX_TASKS="${MAX_TASKS:-1000}"

    exec celery -A $APP -l $LOG_LEVEL -c $CONCURRENCY --maxtasksperchild=$MAX_TASKS worker -Q $QUEUES

else
    
    exec gunicorn --config=gunicorn_config.py backend_test.wsgi
    
fi