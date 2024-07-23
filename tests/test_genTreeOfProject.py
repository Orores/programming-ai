import unittest
import os
import tempfile
from AutoChatBot.genTreeOfProject import DirectoryTreeGenerator

class TestDirectoryTreeGenerator(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.root_dir = self.test_dir.name

        # Create directories and files
        os.makedirs(os.path.join(self.root_dir, 'dir1', 'subdir1'))
        os.makedirs(os.path.join(self.root_dir, 'dir2'))
        os.makedirs(os.path.join(self.root_dir, 'venv'))
        
        open(os.path.join(self.root_dir, 'file1.txt'), 'a').close()
        open(os.path.join(self.root_dir, 'file2.txt'), 'a').close()
        open(os.path.join(self.root_dir, 'dir1', 'file3.txt'), 'a').close()
        open(os.path.join(self.root_dir, 'dir1', 'subdir1', 'file4.txt'), 'a').close()
        open(os.path.join(self.root_dir, 'dir2', 'file5.txt'), 'a').close()
        open(os.path.join(self.root_dir, 'venv', 'file6.txt'), 'a').close()

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def test_generate_tree(self):
        generator = DirectoryTreeGenerator(self.root_dir)
        root_name = os.path.basename(self.root_dir)
        expected_tree = (
            f"{root_name}/\n"
            "    file2.txt\n"
            "    file1.txt\n"
            "    dir2/\n"
            "        file5.txt\n"
            "    dir1/\n"
            "        file3.txt\n"
            "        subdir1/\n"
            "            file4.txt"
        )
        self.assertEqual(generator.generate_tree().strip(), expected_tree)

    def test_ignore_additional_folders(self):
        os.makedirs(os.path.join(self.root_dir, 'custom_ignore'))
        open(os.path.join(self.root_dir, 'custom_ignore', 'file5.txt'), 'a').close()

        generator = DirectoryTreeGenerator(self.root_dir, ignore_patterns=['venv', 'custom_ignore'])
        root_name = os.path.basename(self.root_dir)
        expected_tree = (
            f"{root_name}/\n"
            "    file2.txt\n"
            "    file1.txt\n"
            "    dir2/\n"
            "        file5.txt\n"
            "    dir1/\n"
            "        file3.txt\n"
            "        subdir1/\n"
            "            file4.txt"

        )
        self.assertEqual(generator.generate_tree().strip(), expected_tree)

if __name__ == '__main__':
    unittest.main()
