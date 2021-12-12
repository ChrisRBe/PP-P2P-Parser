# -*- coding: utf-8 -*-
"""
Unit test for the p2p statement class

Copyright 2021-12-12 AlexanderLill
"""
import unittest

from Statement import Statement


class TestStatement(unittest.TestCase):
    """Test case implementation for Statement"""

    def test_value_parsing(self):
        """test parsing of amount value"""

        test_data = [
            ("1.2", 1.2),
            ("1,1", 1.1),
            ("1.000,30", 1000.3),
            ("1,000.30", 1000.3),
            ("1000.30", 1000.3),
        ]

        for item in test_data:
            test_input = item[0]
            expected_output = item[1]
            self.assertEqual(
                expected_output,
                Statement._parse_value(test_input)
            )

if __name__ == '__main__':
    unittest.main()
