from setuptools import setup

setup(
    name='DiscordBot',
    version='0.1.0',
    description='A discord.py bot implementation with dynamic command import',
    author='Nathan Latchaw',
    author_email='natelatchaw@gmail.com',
    license='Creative Commons',
    packages=[
        'bot',
        'bot.database',
        'bot.settings',
    ],
    package_data={
        "bot": [
            "py.typed"
        ],
        "bot.configuration": [
            "py.typed"
        ],
        "bot.database": [
            "py.typed"
        ],
        "bot.settings": [
            "py.typed"
        ],
    },
    url='not available',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Hobbyist',
        'Operating System :: Agnostic',
        'Programming Language :: Python :: 3.10',
    ],
)