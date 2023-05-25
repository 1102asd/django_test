###############
Django Test
###############

本地开发配置
==========

初始化
-------

.. code-block:: bash

    git clone https://github.com/h1608531788/django_test.git
    cd django_test
    pip install "flake8<3.8" bumpversion pep8-naming
    flake8 --install-hook git
    git config --bool flake8.strict true


版本发布
--------

.. code-block:: bash

    bumpversion patch
    git push origin master --tags
    git pull && bumpversion patch && git push origin master --tags
