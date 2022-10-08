import os
import unittest
from revengedit.datparser import ParsingError

from revengedit.consts import EDIT_OPTIONS
from revengedit.value_routines import parse_file

class RevengeditTests(unittest.TestCase):
    def test_read_file(self):
        prefix = "./test/test_files/revenge/"
        for root, dirs, files in os.walk(prefix):
            for file in files:
                self.assertIsInstance(
                    parse_file(f'{prefix}{file}'),
                    dict
                )
                for key in EDIT_OPTIONS:
                    self.assertIn(
                        key,
                        parse_file(f'{prefix}{file}')
                    )

    def test_fail_deluxe_files(self):
        prefix = "./test/test_files/deluxe/"
        for root, dirs, files in os.walk(prefix):
            for file in files:
                with self.assertRaises(ParsingError):
                    parse_file(f'{prefix}{file}')

    def test_fail_non_curv_files(self):
        prefix = "./test/test_files/not_curv/"
        for root, dirs, files in os.walk(prefix):
            for file in files:
                with self.assertRaises(ParsingError):
                    parse_file(f'{prefix}{file}')
