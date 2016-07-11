# -*- coding: utf-8 -*-


def load_config(unittest=False):
    from anyblok import config  # noqa
    from anyblok_pyramid import config  # noqa
    from anyblok_pyramid_beaker import config  # noqa
    from . import config  # noqa
