# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_q',
 'django_q.brokers',
 'django_q.management',
 'django_q.management.commands',
 'django_q.migrations',
 'django_q.tests',
 'django_q.tests.testing_utilities']

package_data = \
{'': ['*'],
 'django_q': ['locale/de/LC_MESSAGES/*',
              'locale/fr/LC_MESSAGES/*',
              'locale/tr/LC_MESSAGES/*']}

install_requires = \
['django-picklefield>=3.1,<4.0', 'django>=3.2']

extras_require = \
{'rollbar': ['django-q-rollbar>=0.1'],
 'sentry': ['django-q-sentry>=0.1'],
 'testing': ['blessed>=1.19.1,<2.0.0',
             'hiredis>=2.0.0,<3.0.0',
             'psutil>=5.9.2,<6.0.0',
             'django-redis>=5.2.0,<6.0.0',
             'iron-mq>=0.9,<0.10',
             'boto3>=1.24.92,<2.0.0',
             'pymongo>=4.2.0,<5.0.0',
             'croniter>=1.3.7,<2.0.0',
             'redis>=4.3.4,<5.0.0']}

entry_points = \
{'djangoq.errorreporters': ['rollbar = django_q_rollbar:Rollbar',
                            'sentry = django_q_sentry:Sentry']}

setup_kwargs = {
    'name': 'django-q2',
    'version': '1.4.2',
    'description': 'A multiprocessing distributed task queue for Django',
    'long_description': "A multiprocessing distributed task queue for Django\n---------------------------------------------------\n\n|image0| |image1| |docs|\n\n::\n\n    Django Q2 is a fork of Django Q. Big thanks to Ilan Steemers for starting this project. Unfortunately, development has stalled since June 2021. Django Q2 is the new updated version of Django Q, with dependencies updates, docs updates and several bug fixes. Original repository: https://github.com/Koed00/django-q\n\nFeatures\n~~~~~~~~\n\n-  Multiprocessing worker pool\n-  Asynchronous tasks\n-  Scheduled, cron and repeated tasks\n-  Signed and compressed packages\n-  Failure and success database or cache\n-  Result hooks, groups and chains\n-  Django Admin integration\n-  PaaS compatible with multiple instances\n-  Multi cluster monitor\n-  Redis, IronMQ, SQS, MongoDB or ORM\n-  Rollbar and Sentry support\n\nRequirements\n~~~~~~~~~~~~\n\n-  `Django <https://www.djangoproject.com>`__ > = 3.2\n-  `Django-picklefield <https://github.com/gintas/django-picklefield>`__\n\nTested with: Python 3.7, 3.8, 3.9, 3.10 Django 3.2.X and 4.1.X\n\nBrokers\n~~~~~~~\n- `Redis <https://django-q2.readthedocs.org/en/latest/brokers.html#redis>`__\n- `IronMQ <https://django-q2.readthedocs.org/en/latest/brokers.html#ironmq>`__\n- `Amazon SQS <https://django-q2.readthedocs.org/en/latest/brokers.html#amazon-sqs>`__\n- `MongoDB <https://django-q2.readthedocs.org/en/latest/brokers.html#mongodb>`__\n- `Django ORM <https://django-q2.readthedocs.org/en/latest/brokers.html#django-orm>`__\n\nInstallation\n~~~~~~~~~~~~\n\n-  Install the latest version with pip::\n\n    $ pip install django-q2\n\n\n-  Add `django_q` to your `INSTALLED_APPS` in your projects `settings.py`::\n\n       INSTALLED_APPS = (\n           # other apps\n           'django_q',\n       )\n\n-  Run Django migrations to create the database tables::\n\n    $ python manage.py migrate\n\n-  Choose a message `broker <https://django-q2.readthedocs.org/en/latest/brokers.html>`__, configure and install the appropriate client library.\n\nRead the full documentation at `https://django-q2.readthedocs.org <https://django-q2.readthedocs.org>`__\n\n\nConfiguration\n~~~~~~~~~~~~~\n\nAll configuration settings are optional. e.g:\n\n.. code:: python\n\n    # settings.py example\n    Q_CLUSTER = {\n        'name': 'myproject',\n        'workers': 8,\n        'recycle': 500,\n        'timeout': 60,\n        'compress': True,\n        'cpu_affinity': 1,\n        'save_limit': 250,\n        'queue_limit': 500,\n        'label': 'Django Q',\n        'redis': {\n            'host': '127.0.0.1',\n            'port': 6379,\n            'db': 0,\n        }\n    }\n\nFor full configuration options, see the `configuration documentation <https://django-q2.readthedocs.org/en/latest/configure.html>`__.\n\nManagement Commands\n~~~~~~~~~~~~~~~~~~~\n\n::\n\n    For the management commands to work, you will need to install Blessed: <https://github.com/jquast/blessed>\n\n\nStart a cluster with::\n\n    $ python manage.py qcluster\n\nMonitor your clusters with::\n\n    $ python manage.py qmonitor\n\nMonitor your clusters' memory usage with::\n\n    $ python manage.py qmemory\n\nCheck overall statistics with::\n\n    $ python manage.py qinfo\n\nCreating Tasks\n~~~~~~~~~~~~~~\n\nUse `async_task` from your code to quickly offload tasks:\n\n.. code:: python\n\n    from django_q.tasks import async_task, result\n\n    # create the task\n    async_task('math.copysign', 2, -2)\n\n    # or with a reference\n    import math.copysign\n\n    task_id = async_task(copysign, 2, -2)\n\n    # get the result\n    task_result = result(task_id)\n\n    # result returns None if the task has not been executed yet\n    # you can wait for it\n    task_result = result(task_id, 200)\n\n    # but in most cases you will want to use a hook:\n\n    async_task('math.modf', 2.5, hook='hooks.print_result')\n\n    # hooks.py\n    def print_result(task):\n        print(task.result)\n\nFor more info see `Tasks <https://django-q2.readthedocs.org/en/latest/tasks.html>`__\n\n\nSchedule\n~~~~~~~~\n\nSchedules are regular Django models. You can manage them through the\nAdmin page or directly from your code:\n\n.. code:: python\n\n    # Use the schedule function\n    from django_q.tasks import schedule\n\n    schedule('math.copysign',\n             2, -2,\n             hook='hooks.print_result',\n             schedule_type=Schedule.DAILY)\n\n    # Or create the object directly\n    from django_q.models import Schedule\n\n    Schedule.objects.create(func='math.copysign',\n                            hook='hooks.print_result',\n                            args='2,-2',\n                            schedule_type=Schedule.DAILY\n                            )\n\n    # Run a task every 5 minutes, starting at 6 today\n    # for 2 hours\n    from datetime import datetime\n\n    schedule('math.hypot',\n             3, 4,\n             schedule_type=Schedule.MINUTES,\n             minutes=5,\n             repeats=24,\n             next_run=datetime.utcnow().replace(hour=18, minute=0))\n\n    # Use a cron expression\n    schedule('math.hypot',\n             3, 4,\n             schedule_type=Schedule.CRON,\n             cron = '0 22 * * 1-5')\n\nFor more info check the `Schedules <https://django-q2.readthedocs.org/en/latest/schedules.html>`__ documentation.\n\n\nTesting\n~~~~~~~\n\nRunning tests is easy with docker compose, it will also start the necessary databases. Just run:\n\n.. code:: bash\n\n    docker-compose -f test-services-docker-compose.yaml run --rm django-q2 poetry run pytest\n\nLocale\n~~~~~~\n\nCurrently available in English, German, Turkish, and French.\nTranslation pull requests are always welcome.\n\nTodo\n~~~~\n\n-  Better tests and coverage\n-  Less dependencies?\n\nAcknowledgements\n~~~~~~~~~~~~~~~~\n\n-  Django Q was inspired by working with\n   `Django-RQ <https://github.com/ui/django-rq>`__ and\n   `RQ <https://github.com/ui/django-rq>`__\n-  Human readable hashes by\n   `HumanHash <https://github.com/zacharyvoase/humanhash>`__\n-  Redditors feedback at `r/django <https://www.reddit.com/r/django/>`__\n\n-  JetBrains for their `Open Source Support Program <https://www.jetbrains.com/community/opensource>`__\n\n.. |image0| image:: https://github.com/GDay/django-q2/actions/workflows/test.yml/badge.svg?branche=master\n   :target: https://github.com/GDay/django-q2/actions?query=workflow%3Atests\n.. |image1| image:: https://coveralls.io/repos/github/GDay/django-q2/badge.svg?branch=master\n   :target: https://coveralls.io/github/GDay/django-q2?branch=master\n.. |docs| image:: https://readthedocs.org/projects/docs/badge/?version=latest\n    :alt: Documentation Status\n    :scale: 100\n    :target: https://django-q.readthedocs.org/\n",
    'author': 'Stan Triepels',
    'author_email': 'django-q2@stantriepels.com',
    'maintainer': 'Stan Triepels',
    'maintainer_email': 'django-q2@stantriepels.com',
    'url': 'https://django-q2.readthedocs.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.14,<4',
}


setup(**setup_kwargs)
