from setuptools import setup, find_packages
version = '0.0.1'


requires = [
    'anyblok',
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
        'ERPBlok': [
            'erpblok-core=erpblok.bloks.erpblok_core:ERPBlokCore',
        ],
    },
    extras_require={},
)
