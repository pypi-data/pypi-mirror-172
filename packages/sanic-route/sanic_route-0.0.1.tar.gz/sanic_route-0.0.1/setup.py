import setuptools
from ran import fs

setuptools.setup(
    name='sanic_route',
    version='0.0.1',
    description='yet a sanic route extension.',
    long_description=fs.load('readme.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/chenshenchao/sanic_route',
    keywords='sanic route',
    license='MIT',
    author='chenshenchao',
    author_email='chenshenchao@outlook.com',
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=setuptools.find_packages(
        exclude=[
            'demo',
            'example',
            'example.*',
        ],
    ),
    install_requires=[
        'sanic==22.9.0'
    ],
)
