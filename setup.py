from setuptools import setup, find_packages
version = '0.0.1'


requires = [
    'anyblok',
    'anyblok_pyramid',
    'pyramid_mako',
    'lxml',
    'rst2html5',
    'python-magic',
]

ERPBlok = [
    'erpblok-core=erpblok.bloks.erpblok_core:ERPBlokCore',
    'erpblok-web-client=erpblok.bloks.erpblok_web_client:ERPBlokWebClient',
    'erpblok-demo=erpblok.bloks.erpblok_demo:ERPBlokDemo',
    'erpblok-debug=erpblok.bloks.erpblok_debug:ERPBlokDebug',
    'erpblok-blok-manager=erpblok.bloks.blok_manager:ERPBlokBlokManager',
]

anyblok_pyramid_includeme = [
    'pyramid_beaker=anyblok_pyramid.pyramid_config:pyramid_beaker',
    'pyramid_config=anyblok_pyramid.pyramid_config:pyramid_config',
    'declare_static=anyblok_pyramid.pyramid_config:declare_static',
    'pyramid_http_config=anyblok_pyramid.pyramid_config:pyramid_http_config',
    'pyramid_jsonrpc_config=anyblok_pyramid.pyramid_config:pyramid_jsonrpc_config',
    'pyramid_mako_and_static=erpblok.pyramid_config:add_mako_and_static',
]

setup(
    name="ERPBlok",
    version=version,
    author="Jean-Sébastien Suzanne",
    author_email="jssuzanne@anybox.fr",
    description="Open Source ERP base on AnyBlok",
    license="GPL3",
    long_description=open('README.rst').read(),
    url="http://docs.erpblok.org/%s" % version,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + ['nose'],
    classifiers=[
    ],
    entry_points={
        'console_scripts': [
            'erpblok=erpblok.scripts:wsgi',
        ],
        'bloks': ERPBlok,
        'anyblok_pyramid.includeme': anyblok_pyramid_includeme,
    },
    extras_require={},
)
