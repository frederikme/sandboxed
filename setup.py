import setuptools
from distutils.core import setup

setup(
  name='sandboxed',         # How you named your folder
  packages=['sandboxed'],   # Chose the same as "name"
  version='2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='Sandbox/Virtual Machine detection',   # Give a short description about your library
  author='Frederik Mees',                   # Type in your name
  author_email='frederik.mees@gmail.com',      # Type in your E-Mail
  url='https://github.com/frederikme/sandbox-evasion',   # Provide either the link to your github or to your website
  download_url='https://github.com/frederikme/sandbox-evasion/archive/2.0.tar.gz',    # I explain this later on
  keywords=['Sandbox', 'Virtual machine', 'Virtualbox', 'detection'],   # Keywords that define your project best
  install_requires=['psutil', 'requests', 'pypiwin32; platform_system == "Windows"'],

  package_data={},

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your loadingz
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
