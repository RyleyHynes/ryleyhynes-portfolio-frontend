#!/usr/bin/env python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    project_root = Path(__file__).resolve().parent
    env_file = project_root / '.env.local'
    load_dotenv(env_file)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
