import unittest
import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Return a list of related pages between two pdfs.')
    parser.add_argument('captain', type=str)
    args = parser.parse_args(argv)
    settings = vars(args)
    return settings

class TestTribbify(unittest.TestCase):
    def test(self):
        pass

    def test_main(self):
        main(["test"])

if __name__ == "__main__":
    unittest.main()
