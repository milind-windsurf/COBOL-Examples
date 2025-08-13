#!/usr/bin/env python3
"""
Basic tests for the custom shell
"""

import unittest
import os
import tempfile
from shell import CustomShell


class TestCustomShell(unittest.TestCase):
    def setUp(self):
        self.shell = CustomShell()
        
    def test_expand_variables(self):
        """Test environment variable expansion"""
        os.environ['TEST_VAR'] = 'test_value'
        result = self.shell.expand_variables('echo $TEST_VAR')
        self.assertEqual(result, 'echo test_value')
        
    def test_expand_aliases(self):
        """Test alias expansion"""
        result = self.shell.expand_aliases('ll')
        self.assertEqual(result, 'ls -la')
        
    def test_parse_command(self):
        """Test command parsing"""
        segments = self.shell.parse_command('ls -la | grep test')
        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0], ['ls', '-la'])
        self.assertEqual(segments[1], ['grep', 'test'])
        
    def test_builtin_pwd(self):
        """Test pwd builtin"""
        import io
        import sys
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.shell.builtin_pwd()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()
        
        self.assertEqual(output, os.getcwd())


if __name__ == '__main__':
    unittest.main()