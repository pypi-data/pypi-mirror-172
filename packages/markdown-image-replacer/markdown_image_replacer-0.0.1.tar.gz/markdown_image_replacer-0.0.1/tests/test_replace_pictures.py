import unittest
import os

from replace_pictures import MdImageReplacer


class TestMdImageReplacer(unittest.TestCase):

    def test_init(self):
        self.cwd = os.getcwd()
        with self.assertRaises(RuntimeError):
            MdImageReplacer('/no_such_file')

        mip = MdImageReplacer('tests/data/test.md')
        self.assertEqual(mip.typora_root, os.path.join(self.cwd, "tests/data/static"))
        self.assertEqual(len(mip.find_all_picture_needles()), 4)

        print(mip.replace_pictures(os.path.join(os.getcwd(), "abc"), "def"))
        mip.dump("t.md", os.path.join(os.getcwd(), "abc"), "def")

    def test_target_dir(self):
        print("/i/".split('/i/'))
        print(os.path.abspath('.'))


if __name__ == '__main__':
    unittest.main()

