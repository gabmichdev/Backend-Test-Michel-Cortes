import os

from celery import Celery

from .envtools import getenv


class CelerySettings:
    # Settings for version 4.3.0
    # see: https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html
    # important note: config var names do not match perfectly with celery doc, keep that in mind.
    # General settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#general-settings
    CELERY_ACCEPT_CONTENT = ["json"]
    # Time and date settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#time-and-date-settings
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = "UTC"
    # Task settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-settings
    CELERY_TASK_SERIALIZER = "json"
    # Task execution settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-execution-settings
    CELERY_ALWAYS_EAGER = getenv("CELERY_ALWAYS_EAGER", default="False", coalesce=bool)
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = getenv(
        "CELERY_EAGER_PROPAGATES_EXCEPTIONS", default="False", coalesce=bool
    )
    CELERY_IGNORE_RESULT = getenv("CELERY_IGNORE_RESULT", default="True", coalesce=bool)
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERYD_TASK_TIME_LIMIT = 60 * 2  # hard time limit
    CELERYD_TASK_SOFT_TIME_LIMIT = int(CELERYD_TASK_TIME_LIMIT * 0.85)
    CELERY_ACKS_LATE = True
    CELERY_TASK_REJECT_ON_WORKER_LOST = True
    # Task result backend settings
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#task-result-backend-settings
    CELERY_RESULT_BACKEND = getenv(
        "CELERY_RESULT_BACKEND_URL", default="redis://redis:6379/3"
    )
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
    # Message Routing
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#message-routing
    # BROKER_TASK_QUEUE_HA_POLICY = []
    CELERY_DEFAULT_QUEUE = "celery"
    CELERY_DEFAULT_EXCHANGE = CELERY_DEFAULT_QUEUE
    CELERY_DEFAULT_ROUTING_KEY = CELERY_DEFAULT_QUEUE
    # Message Routing
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#broker-url
    BROKER_URL = getenv("CELERY_BROKER_URL", default="redis://redis:6379/2")
    BROKER_POOL_LIMIT = 10  # default is 10
    BROKER_CONNECTION_MAX_RETRIES = 0  # default is 100, ask joe why 0
    BROKER_HEARTBEAT = None
    # Worker
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#worker
    CELERYD_WORKER_LOST_WAIT = 20
    # Logging
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#logging
    CELERYD_HIJACK_ROOT_LOGGER = getenv(
        "CELERYD_HIJACK_ROOT_LOGGER", default="False", coalesce=bool
    )
    # Custom Component Classes (advanced)
    # https://docs.celeryproject.org/en/v4.3.0/userguide/configuration.html#custom-component-classes-advanced
    CELERYD_POOL_RESTARTS = True


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_test.settings")

settings = CelerySettings()

app = Celery("backend_test")
app.config_from_object(settings)
app.autodiscover_tasks()
