from setuptools import setup

setup(
    name='nomad-diff',
    version='1.0.0',
    description='Nomad job diff formatter in Python',
    author='Strigo.io',
    author_email='ops@strigo.io',
    python_requires='>=3.7',
    url='https://github.com/strigo/nomad-diff',
    packages=['nomad_diff'],
    install_requires=[
        'pydantic~=1.8.1',
        'colorama~=0.4.4',
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
    ],
)
