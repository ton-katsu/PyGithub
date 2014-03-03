# -*- coding: utf-8 -*-

# Copyright 2013-2014 Vincent Jacques <vincent@vincent-jacques.net>

"""
`Pagination <http://developer.github.com/v3/#pagination>`_ is implemented in PyGithub by :class:`.PaginatedList`.
You should use this class as a classic Python
`iterator type <http://docs.python.org/2/library/stdtypes.html?highlight=__iter__#iterator-types>`_.

..  Authenticate for doctest but don't show it in the doc
    >>> import PyGithub
    >>> import GithubCredentials
    >>> g = PyGithub.BlockingBuilder().Login(GithubCredentials.login, GithubCredentials.password).Build()

Example::

    >>> user = g.get_authenticated_user()
    >>> repositories = user.get_repos()  # repositories is a PaginatedList
    >>> for repo in repositories:
    ...     print repo.full_name  # doctest: +ELLIPSIS
    jacquev6/ActionTree
    jacquev6/AnotherPyGraphvizAgain
    ...
    jacquev6/ViDE
    jacquev6/vincent-jacques.net

or shorter::

    >>> for repo in user.get_repos():
    ...     print repo.full_name  # doctest: +ELLIPSIS
    jacquev6/ActionTree
    jacquev6/AnotherPyGraphvizAgain
    ...
    jacquev6/ViDE
    jacquev6/vincent-jacques.net

You can also build a list from a PaginatedList (all the subsequent requests to GitHub will be performed
during the conversion instead of lazilly during the iteration)::

    >>> repositories = list(user.get_repos())  # repositories is a plain list

GitHub provide no way to know the number of items a paginated request will return, so PaginatedList has no
length::

    >>> len(user.get_repos())
    Traceback (most recent call last):
    ...
    TypeError: object of type 'PaginatedList' has no len()


If you really mean to take the length of a PaginatedList, you have to explicitelly construct a list and then use its length::

    >>> len(list(user.get_repos()))
    25

But often, there is an attribute in the parent object::

    >>> user.public_repos
    22
    >>> user.owned_private_repos
    3

For reference, see :class:`.PaginatedList`.
"""

import sys


class PaginatedList(object):
    """
    Class abstracting `paginated requests <http://developer.github.com/v3/#pagination>`_. See the :ref:`User Guide <pagination_foo>` for an introduction.

    See also :meth:`.Builder.PerPage`.
    """

    def __init__(self, klass, session, verb, url, urlArguments):
        self.__contentClass = klass
        self.__session = session
        self.__verb = verb
        self.__url = url
        self.__elements = []
        if "per_page" not in urlArguments:
            if session.PerPage is not None:
                urlArguments["per_page"] = session.PerPage
        self.__grow(urlArguments)

    def __getitem__(self, index):
        if isinstance(index, slice):
            start = 0 if index.start is None else index.start
            stop = sys.maxsize if index.stop is None else index.stop
            self.__growToIndex(max(start, stop))
        else:
            self.__growToIndex(index)
        return self.__elements[index]

    def __growToIndex(self, index):
        while len(self.__elements) <= index and self.__url is not None:
            self.__grow({})

    def __grow(self, urlArguments):
        r = self.__session._request("GET", self.__url, urlArguments)
        self.__url = r.links.get("next", {"url": None})["url"]
        self.__elements += [self.__contentClass(self.__session, e, None) for e in r.json()]

# @todoAlpha class PaginatedListWithPages(PaginatedList):
    # def get_page(self, i):