"""
The main entry point.
Invoke as `notion-gcal-sync' or `python -m notion-gcal-sync'
or 'python -m notion_gcal_sync.__main__
"""
import logging

from notion_gcal_sync.install import configure

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    from notion_gcal_sync.core import sync

    cfg = configure()
    sync(cfg)


if __name__ == "__main__":
    main()
