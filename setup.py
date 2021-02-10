from setuptools import setup, find_packages

setup(
    name='website_monitor',
    version='0.0.1',
    packages=find_packages(),
    author='Mikhail Medvedev',
    author_email='moorck84@gmail.com',
    description='Website availability monitor that works with Aiven services',
    setup_requires=['pytest-runner'],
    test_suite='tests',
    install_requires=[
        'kafka-python==2.0.2',
        'requests==2.25.1',
        'psycopg2-binary==2.8.6',
    ],
    tests_require=[
        'pytest==6.2.2',
        'pytest-cov==2.11.1',
        'responses==0.12.1',
    ],
    entry_points={
        'console_scripts': [
            'monitor=website_monitor:main'
        ]
    }
)
