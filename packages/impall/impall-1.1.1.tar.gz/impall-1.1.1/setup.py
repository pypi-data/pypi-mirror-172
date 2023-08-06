# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['impall']
setup_kwargs = {
    'name': 'impall',
    'version': '1.1.1',
    'description': 'Try to import all modules below a given root',
    'long_description': "``impall``: Automatically import everything\n-------------------------------------------------------------\n\nA three-line unit test in your project automatically imports\nevery Python file and module in it, optionally testing for warnings.\n\nWhy?\n=====\n\nNot every file is covered by unit tests; and unit tests won't report any new\nwarnings that occur.\n\n``impall`` is a single-file library with a unit test that automatically\nimports every Python file and module in your project.\n\nI drop ``include_all`` into each new project.  It takes seconds, it inevitably\ncatches lots of dumb problems early, and it requires no maintenance.\n\n\nHow to use ``impall``\n==============================\n\nInstall it with ``pip install impall``, and use it by adding\n`this tiny file <https://github.com/rec/impall/blob/master/all_test.py>`_\n(`raw <https://raw.githubusercontent.com/rec/impall/master/all_test.py>`_)\nanywhere in a project - it looks like this:\n\n.. code-block:: python\n\n    import impall\n\n\n    class ImpAllTest(impall.ImpAllTest):\n        pass\n\nand most of the time that's all you need.\n\nOverriding properties\n=============================\n\nImpAllTest has eight properties that can be overridden.\n\n  * CLEAR_SYS_MODULES: If `True`, `sys.modules` is reset after each import.\n  * EXCLUDE: A list of modules that will not be imported at all.\n  * FAILING: A list of modules that must fail.\n  * INCLUDE: If non-empty, exactly the modules in the list will be loaded.\n  * MODULES: If False, search all subdirectories.\n  * PATHS: A list of paths to search from.\n  * RAISE_EXCEPTIONS: If True, stop importing at the first exception\n  * WARNINGS_ACTION: One of: default, error, ignore, always, module, once\n\nFull documentation for each property is `here\n<https://github.com/rec/impall/blob/master/impall.py#L18-L133>`_.\n\nTo permanently override a test property, set it in the derived class, like\nthis:\n\n.. code-block:: python\n\n    import impall\n\n\n    class ImpAllTest(impall.ImpAllTest):\n        WARNINGS_ACTION = 'error'\n\n\nTo temporarily override a test property, set an environment variable before\nrunnning the test, like this:\n\n.. code-block:: bash\n\n    $ _IMPALL_WARNINGS_ACTION=error pytest\n\nUsing ``impall.py`` as a standalone program\n\nThe file ``impall.py`` is executable and is installed in the path by\n``pip``.  You can use it on projects that you are evaluating or debugging\nlike this:\n\n.. code-block:: bash\n\n    $ impall.py [directory ..directory]\n\nwhere if no directory is specified it uses the current directory.\n\nYou can use environment variables to set properties as above and for convenience\nthere are also command line flags for each property, so you can write:\n\n.. code-block:: bash\n\n    $ impall.py --catch_exceptions --all_directories --exclude=foo/bar\n",
    'author': 'Tom Ritchford',
    'author_email': 'tom@swirly.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rec/impall',
    'py_modules': modules,
}


setup(**setup_kwargs)
