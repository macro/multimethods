# -*- coding: utf-8 -*-

"""
Multimethods

An implementation of multimethods for Python, heavily influenced by
the Clojure programming language.

Copyright (C) 2010-2011 by Daniel Werner.

See the README file for information on usage and redistribution.
"""

import functools


class DefaultMethod(object):
    """
        Class of singleton object allowing default MultiMethod.
    """
    def __repr__(self):
        return '<DefaultMethod>'

Default = DefaultMethod()


def get_multimethod_key(*args, **kwargs):
    """
        Creates immutable key out of args and kwargs.
    """
    return tuple(map(repr, args) + map(repr, kwargs.itervalues()))

class MultiMethod(object):
    __instances__ = {}

    def __init__(self, name, dispatch_func=None):
        if name in self.__class__.__instances__:
            raise Exception("A multimethod '%s' already exists, "
                            "redeclaring it would wreak havoc" % name)
        self.dispatch_func = dispatch_func or get_multimethod_key
        self.methods = {}
        self.default_method = None
        self.__name__ = name
        self.__class__.__instances__[name] = self

    def __call__(self, *args, **kwargs):
        dispatch_key = self.dispatch_func(*args, **kwargs)
        if dispatch_key in self.methods:
            return self.methods[dispatch_key](*args, **kwargs)
        if self.default_method is not None:
            return self.default_method(*args, **kwargs)
        raise Exception("No matching method on multimethod '%s' and "
                        "no default method defined" % self.__name__)

    def add_method(self, func, *args):
        if args == (Default,):
            self.default_method = func
        else:
            dispatch_key = get_multimethod_key(*args)
            self.methods[dispatch_key] = func

    def remove_method(self, dispatch_val):
        del self.methods[dispatch_val].multimethod
        del self.methods[dispatch_val]

    def methods(self):
        return self.methods

    def __repr__(self):
        return "<MultiMethod '%s'>" % self.__name__


def method(*args):
    def method_decorator(func):
        """
           Decorator which registers a function as a new method of a like-named
           multimethod, keyed by dispatch_val.  The multimethod is determined by
           taking the method's name up to the last occurence of '__',
           e.g. function foo_bar__zig will become a method on the foo_bar
           multimethod.
        """
        try:
            multimethod = MultiMethod.__instances__[func.__name__]
        except KeyError:
            # create multimethod (don't require registration)
            multimethod = MultiMethod(func.__name__)
        functools.update_wrapper(multimethod, func)
        multimethod.add_method(func, *args)
        return multimethod
    return method_decorator

__all__ = ['MultiMethod', 'method', 'Default']
