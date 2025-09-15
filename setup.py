from setuptools import setup, find_packages

setup(
    name="gitcord",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "discord.py>=2.3.0",
        "flask>=2.3.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'gitcord=src.bot.main:main',
        ],
    },
)
