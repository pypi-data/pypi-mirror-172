"""Extra utils used internally and within EnviDat projects."""

import logging
import os
import sys
from pathlib import Path
from typing import NoReturn, Union

import requests

log = logging.getLogger(__name__)


def _debugger_is_active() -> bool:
    """Check to see if running in debug mode.

    Returns:
        bool: if a debug trace is present or not.
    """
    gettrace = getattr(sys, "gettrace", lambda: None)
    return gettrace() is not None


def load_dotenv_if_in_debug_mode(env_file: Union[Path, str]) -> NoReturn:
    """Load secret .env variables from repo for debugging.

    Args:
        env_file (Union[Path, str]): String or Path like object pointer to
            secret dot env file to read.
    """
    try:
        from dotenv import load_dotenv
    except ImportError as e:
        log.error(
            """
            Unable to import dotenv.
            Note: The logger should be invoked after reading the dotenv file
            so that the debug level is by the environment.
            """
        )
        log.error(e)
        raise ImportError(
            """
            Unable to import dotenv, is python-dotenv installed?
            Try installing this package using pip install envidat[dotenv].
            """
        )

    if _debugger_is_active():
        secret_env = Path(env_file)
        if not secret_env.is_file():
            log.error(
                """
                Attempted to import dotenv, but the file does not exist.
                Note: The logger should be invoked after reading the dotenv file
                so that the debug level is by the environment.
                """
            )
            raise FileNotFoundError(
                f"Attempted to import dotenv, but the file does not exist: {env_file}"
            )
        else:
            load_dotenv(secret_env)


def get_logger() -> logging.basicConfig:
    """Set logger parameters with log level from environment.

    Note:
        Defaults to DEBUG level, unless specified by LOG_LEVEL env var.
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", default="DEBUG"),
        format=(
            "%(asctime)s.%(msecs)03d [%(levelname)s] "
            "%(name)s | %(funcName)s:%(lineno)d | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    log.debug("Logger set to STDOUT.")


def get_url(url: str) -> requests.Response:
    """Get a URL with additional error handling.

    Args:
        url (str): The URL to GET.
    """
    try:
        log.debug(f"Attempting to get {url}")
        r = requests.get(url)
        r.raise_for_status()
        return r
    except requests.exceptions.ConnectionError as e:
        log.error(f"Could not connect to internet on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.HTTPError as e:
        log.error(f"HTTP response error on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.RequestException as e:
        log.error(f"Request error on get: {r.request.url}")
        log.error(f"Request: {e.request}")
        log.error(f"Response: {e.response}")
    except Exception as e:
        log.error(e)
        log.error(f"Unhandled exception occured on get: {r.request.url}")

    return None
