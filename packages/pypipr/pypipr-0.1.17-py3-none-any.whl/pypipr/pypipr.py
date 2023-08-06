PYPIPR = True

"""PYPIPR Module"""

"""PYTHON Standard Module"""

"""PYPI Module"""


class Pypipr:
    @staticmethod
    def test_print():
        """Print simple text to test this module is working"""
        print("Hello from PyPIPr")


def sets_ordered(iterator):
    """
    Hanya mengambil nilai unik dari suatu list
    """
    r = {i: {} for i in iterator}
    for i, v in r.items():
        yield i


def list_unique(iterator):
    """Sama seperti sets_ordered()"""
    return sets_ordered(iterator)


def chunck_array(array, size, start=0):
    """
    Membagi array menjadi potongan-potongan sebesar size
    """
    for i in range(start, len(array), size):
        yield array[i : i + size]
