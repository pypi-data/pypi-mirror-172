pygitsync
=========

A utility to poll a remote git repository and maintain local state according
simple rules such as the HEAD of a specified branch, or the latest tag
conforming to a regular expression.

.. contents::

.. section-numbering::


Installation
------------

The ``pygitsync`` package is available from PyPI. Installing into a virtual
environment is recommended.

.. code-block::

   python3 -m venv .venv; .venv/bin/pip install pygitsync


Credential management
---------------------

One relatively straight-forward means of managing credentials for SSH based
access to git repositories is using ``ssh-agent``. Before starting the
``git-sync`` process, take the following steps.

.. code-block::

   eval $(ssh-agent)
   ssh-add <path to keyfile to be used by pygitsync>
   # type the passphrase for your SSH key as prompted
   git-sync [options]

``git-sync`` will now use the ssh agent session to acquire access to the SSH key.

Having a human type in a passphrase may not work very well for automation, so
further effort will likely be needed to automatically acquire the passphrase
from some kind of encrypted vault, and then apply that passphrase to the ssh
agent session. A work-around may be to use an empty-passphrase SSH key, but
this is not recommended at all for maintaining good security.


Getting started
---------------

Having just installed ``pygitsync`` you really just want to get a remote repo
syncing, right? You need to create a configuration file - the default location is
``.pygitsync.yaml`` and it needs to look something like this. In this case
we're just syncing the default (main) branch of the pygitsync repo itself.

.. code-block::

   ---
   repo:
     pattern_type: branch
     pattern: main
     url: git@gitlab.com:ci-cd-devops/pygitsync.git
   application:
     exception_sleep_seconds: 10
     is_daemon: false
     sleep_interval_seconds: 30

Using this configuration the remote repo will be pulled every 30 seconds to
check for updates in the main branch. The pattern type "branch" means that the
sync will always update to the latest HEAD pulled from the remote. Disabling
the ``is_daemon`` setting means that the process will run indefinitely in the
foreground (useful to run inside containers).

Running indefinitely means that the process will never exit for exceptions. If
an exception occurs very early in the process then the exception handling loop
could run very quickly, consuming large amounts of needless CPU. The
``exception_sleep_seconds`` setting puts a delay in that exception handling
oop to prevent such a scenario from occurring.

The repo will be initially be cloned to the current working directory of the
``git-sync`` executable, or use the ``--working`` argument to specify an
alternate location for the repo working directory.

Take a look at other configuration arguments using ``git-sync --help``.
