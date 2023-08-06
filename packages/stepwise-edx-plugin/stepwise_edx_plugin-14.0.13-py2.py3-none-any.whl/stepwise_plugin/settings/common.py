"""
Common Pluggable Django App settings

Handling of environment variables, see: https://django-environ.readthedocs.io/en/latest/
to convert .env to yml see: https://django-environ.readthedocs.io/en/latest/tips.html#docker-style-file-based-variables
"""
from path import Path as path
import environ
import os


# path to this file.
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ROOT = path(__file__).abspath().dirname().dirname()  # /blah/blah/blah/.../stepwise_plugin
REPO_ROOT = APP_ROOT.dirname()  # /blah/blah/blah/.../stepwise-edx-plugin
TEMPLATES_DIR = APP_ROOT / "templates"

environ.Env.read_env(os.path.join(REPO_ROOT, ".env"))


def plugin_settings(settings):
    """
    Injects local settings into django settings
    """
    settings.MAKO_TEMPLATE_DIRS_BASE.extend([TEMPLATES_DIR])  # noqa: F841
