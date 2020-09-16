import os
from setuptools import setup

setup(
    name='django_video_embedding',
    version='0.1.1',
    description='Support for video upload in Django models',
    long_description='Support for video upload in Django models',
    author='4Sigma',
    author_email='info@4sigma.it',
    url='https://github.com/vokai/django-video-embedding',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='django video model field',
    install_requires=['Django >= 2'],
    packages=['django_video_embedding'],
)
