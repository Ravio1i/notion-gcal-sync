"""
The main entry point.
Invoke as `notion-gcal-sync' or `python -m notion-gcal-sync'
or 'python -m notion_gcal_sync.__main__
"""
import os

current_dir = os.path.dirname(__file__)


def main():
    from notion_gcal_sync.core import main
    main()


if __name__ == '__main__':
    import sys
    sys.exit(main())
