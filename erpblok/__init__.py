# -*- coding: utf-8 -*-


def load_config():
    from . import config  # noqa
    from .client import homepage  # noqa
    from .client import database  # noqa
    from .client import login  # noqa
    from .client import web  # noqa
