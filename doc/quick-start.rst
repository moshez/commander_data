Getting Started
================

The
:code:`commander_data`
library helps produce valid command-lines
for functions such as
:code:`subprocess.run`.
While allowing for any possible command-line,
it tries to produce
"typical"
commands in a more Pythonic way.

For example, to create a new virtual environment:

.. code::

    import subprocess
    from commander_data import COMMAND
    
    subprocess.run(COMMAND.python(m=None).venv("my-env"))

This will run
``python -m venv my-env``.
It is equivalent to

.. code::

    import subprocess
    
    subprocess.run(["python", "-m", "venv", "my-env"])

Helpful prefixes can be stored in variables:

.. code::

    import commander_data import COMMAND
    import subprocess
    
    GIT = COMMAND.git
    
    subprocess.run(GIT.commit(message="quick commit"))
    subprocess.run(GIT.push())
    