# -*- encoding: utf-8 -*-
# ! python3

import os
import sys
from pathlib import Path

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_test_application.settings")

    # This adds tests directory to the PYTHONPATH
    current_path = Path(__file__).parent.parent.resolve()
    sys.path.append(str(current_path))

    execute_from_command_line(sys.argv)
