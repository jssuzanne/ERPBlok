from setuptools import setup, find_packages
version = '0.0.1'


requires = [
    'anyblok',
    'anyblok_pyramid',
    'anyblok_pyramid_beaker',
    'pyramid_rpc',
    'pyramid_mako',
    'lxml',
    'rst2html5',
    'python-magic',
    'gunicorn',
    'passlib',
]

ERPBlok = [
    'erpblok-core=erpblok.bloks.erpblok_core:ERPBlokCore',
    'erpblok-web-client=erpblok.bloks.erpblok_web_client:ERPBlokWebClient',
    'erpblok-demo=erpblok.bloks.erpblok_demo:ERPBlokDemo',
    'erpblok-debug=erpblok.bloks.erpblok_debug:ERPBlokDebug',
    'erpblok-blok-manager=erpblok.bloks.blok_manager:ERPBlokBlokManager',
]

anyblok_pyramid_includeme = [
    'mako_and_static=erpblok.pyramid_config:add_mako_and_static',
    'declare_json_adapter=erpblok.pyramid_config:declare_json_data_adapter',
    'load_main_client=erpblok.client:load_client',
]

anyblok_init = [
    'load_config=erpblok:load_config',
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
        'bloks': ERPBlok,
        'anyblok_pyramid.includeme': anyblok_pyramid_includeme,
        'anyblok.init': anyblok_init,
    },
    extras_require={},
)
