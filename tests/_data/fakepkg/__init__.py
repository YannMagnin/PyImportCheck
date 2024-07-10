"""
test
"""
__all__ = [
    'b_test2',
    'b_test1',
]

print('a')
from fakepkg.a import a_test1
print('b')
from fakepkg.b import b_test1, b_test2
print('c')
