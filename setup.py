from setuptools import setup

setup(name='SpeedRunTimersWebsite',
      version='0.1-dev',
      licence='MIT',
      description='A Flask based project for distributing and participating in races.',
      author='Davis Robertson',
      author_email='davis@daviskr.com',
      url='https://github.com/EpicDavi/SpeedRunTimersWebsite',
      install_requires=['flask', 'flask-sqlalchemy', 'flask-wtf', 'flask-login']
     )
