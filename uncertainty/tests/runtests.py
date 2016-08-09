import os
import sys

import django
from django.test.utils import get_runner
from django.conf import settings


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'uncertainty.tests.settings'
    django.setup()
    sys.path.insert(0, os.path.dirname(__file__))
    test_runner = get_runner(settings)()
    failures = test_runner.run_tests([], verbosity=1, interactive=True)
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
