from distutils.core import setup
setup(
  name = 'thread_lfanke',         # How you named your package folder (MyLib)
  packages = ['thread_lfanke'],   # Chose the same as "name"
  version = '0.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = '简单封装threading的线程',   # Give a short description about your library
  author = 'Lfan_ke',                   # Type in your name
  author_email = 'chengkelfan@foxmail.com',      # Type in your E-Mail
  keywords = ['Thread'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
