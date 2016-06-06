from fabric.api import local


def lint():
    local('pep8 --ignore=E501 fabfile.py')
    local('pep8 --ignore=E402,E501 stringer_api/__init__.py')
    local('pep8 --ignore=E501 --exclude=stringer_api/__init__.py stringer_api/')
