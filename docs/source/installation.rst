Installation
===============

Installation documentation is written under Windows as if you're using Linux, you can probably already do this by
yourself without any help.

.. note:: There is no official MacOS support, while it *may* work, it's not a guarantee and no help will be provided
   for it.

Prerequisites
----------------

Make sure you have a version of Python 3.X installed on your system and added to PATH.
If you don't have it installed, you can do so by going to the `Official Website <https://www.python.org>`__ and finding
a version of Python greater or equal to 3.7.

Download
----------------

Navigate to the `GitHub Releases Page <https://www.github.com/TheodoreHua/ClaimDoneRemover/releases/latest>`__ and
scroll down to the assets section. If a file named `ClaimDoneRemover_X.X.X.zip` is listed there, download that.
If it isn't, download the file named `Source code (zip)`.

Once you've downloaded it, extract the ZIP file into a folder of your choice.

Requirements
----------------

Open up a command prompt window and navigate to the folder in which you installed CDR (a quick way of doing so is
opening the folder in Windows Explorer, clicking the address bar, and entering `cmd` which will automatically open
a command prompt window in that directory).

Using PyPi
^^^^^^^^^^^

Once you've opened a command prompt window up in the folder, enter `pip install -r requirements.txt`.

.. note:: If you have multiple Python applications on your machine that has conflicting requirements, you may need to
    use a virtualenv, you can find many resources online on how to use them. You could also use poetry instead (see
    below)

Wait for the command to finish and make sure there's no errors.

Using Poetry
^^^^^^^^^^^^^

`Poetry <https://python-poetry.org/>`__ is a much easier way to manage dependencies, if it's installed. Installation is
actually pretty simple, `see here for a guide <https://python-poetry.org/docs/#installation>`__.

Once you have poetry installed, you can open a command prompt window up in the folder and enter `poetry install`.

Wait for the command to finish, and make sure there's no errors.

Next Step
---------------

That wraps up the installation segment, you can now proceed to `Setup <setup.html>`_
