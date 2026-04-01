from setuptools import setup

setup(
    name='diamond',
    version='0.1',
    py_modules=['diamond', 'lexer', 'expression_parser'],
    entry_points={
        'console_scripts': [
            'diamond = diamond:main',  # maps `diamond` to diamond.py:main()
        ],
    },
    author="Your Name",
    description="A custom scripting language called Diamond Lang",
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
