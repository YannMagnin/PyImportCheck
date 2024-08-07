"""
a   - A test
"""
__all__ = [
    'ACls',
    'a_test2',
]

print('-== FROM TEST IMPORT B_TEST1')


# success
#from test.b import b_test1

# import error (circular dependency)
#from test import b_test1
import fakepkg

print('before ACls')
class ACls():
    """ osef """
    fakepkg.b_test1()

print('befor a_test2')
def a_test2() -> None:
    """ osef """
