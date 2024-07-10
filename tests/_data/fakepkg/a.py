"""
a   - A test
"""
__all__ = [
    'a_test1',
    'a_test2',
]

print('-== FROM TEST IMPORT B_TEST1')


# success
#from test.b import b_test1

# import error (circular dependency)
#from test import b_test1
import fakepkg

print('before a_test1')
def a_test1() -> None:
    """ osef """
    fakepkg.b_test1()

print('befor a_test2')
def a_test2() -> None:
    """ osef """
