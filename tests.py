import unittest

from multimethods import MultiMethod, method, Default


class PatternMatchingTests(unittest.TestCase):

    def test_arg_type(self):
        """
        Tests pattern match of arg types
        """
        combine = MultiMethod('combine', lambda *x: tuple(map(repr,
                        map(type, x))))

        @method(int, int)
        def combine(x, y):
            return x * y

        @method(str, str)
        def combine(x, y):
            return x + ' & ' + y

        self.assertEqual(combine(31,2), 62)
        self.assertEqual(combine('foo','bar'), 'foo & bar')

    def test_no_default(self):
        """
        Tests exception is raised when no multimethod is matched and
        no default is defined
        """
        foobar = MultiMethod('foobar')
        self.assertRaises(Exception, foobar, 1.2, 1.3)

    def test_default(self):
        """
        Tests exception is not raised when no multimethod is matched and
        default is defined
        """
        @method(Default)
        def combine(x, y):
            return x * y

        self.assertEqual(combine(31,2), 62)
        self.assertEqual(combine('a',2), 'aa')

    def test_default_dispatch(self):
        """
        Tests use of default dispatcher which uses repr.
        """
        @method([])
        def multi_len(l):
            return 0

        @method(Default)
        def multi_len(l):
            return 1 + multi_len(l[1:])

        self.assertEqual(multi_len(list('abcdefghijklmnopqrstuvwxyz')), 26)

    def test_object_list(self):
        """
        Tests pattern match of list of objects
        """
        predicate_filter = MultiMethod('predicate_filter',
                lambda x, y : tuple([repr(x)]))

        even = lambda x: x % 2 == 0
        odd = lambda x: x % 2 != 0

        @method([even])
        def predicate_filter(predicates, l):
            return filter(even, l)

        @method([odd])
        def predicate_filter(predicates, l):
            return filter(odd, l)

        @method([even, odd])
        def predicate_filter(predicates, l):
            return list(l)

        self.assertEqual(predicate_filter([odd], xrange(1,5)), [1,3])
        self.assertEqual(predicate_filter([even], xrange(1,5)), [2,4])
        self.assertEqual(predicate_filter([even, odd], xrange(1,5)), [1,2,3,4])

