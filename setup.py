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
    },
    extras_require={},
)
