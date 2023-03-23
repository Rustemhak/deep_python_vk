"""Tests for filter_file module"""
import io
import os
import unittest
from generator_filter import read_file_with_filter


class TestReadFileWithFilter(unittest.TestCase):
    """Tests for read_file_with_filter function"""

    def test_read_file_with_filter_search_words_is_none_ok(self):
        """Test when search_words is None. Returns all file's rows"""
        lines = ['Vestibulum antE', 'Ipsum Primis']
        search_words = None
        with (io.StringIO()) as file_obj:
            file_obj.write(os.linesep.join(lines))
            file_obj.seek(0)
            result_lines = list(read_file_with_filter(file_obj, search_words))

        self.assertEqual(result_lines, lines)

    def test_read_file_with_filter_lower_case_ok(self):
        """Test when search_word in one of line"""
        lines = ['vestibulum ante', 'ipsum primis']
        search_words = ['primis']
        with (io.StringIO()) as file_obj:
            file_obj.write(os.linesep.join(lines))
            file_obj.seek(0)
            result_lines = list(read_file_with_filter(file_obj, search_words))

        self.assertEqual(result_lines, ['ipsum primis'])

    def test_read_file_with_filter_any_case_ok(self):
        """Test when search_word in one of line, different char's cases"""
        lines = ['Vestibulum antE', 'Ipsum Primis']
        search_words = ['primis']
        with (io.StringIO()) as file_obj:
            file_obj.write(os.linesep.join(lines))
            file_obj.seek(0)
            result_lines = list(read_file_with_filter(file_obj, search_words))

        self.assertEqual(result_lines, ['Ipsum Primis'])

    def test_read_file_with_filter_several_search_similar_words_ok(self):
        """Test when line contains word similar for search words"""
        lines = ['Vestibulum anTe', 'ipsum primis',
                 'In faucibus', 'orci luctus aneT']
        search_words = ['faucibus', 'ante']
        with (io.StringIO()) as file_obj:
            file_obj.write(os.linesep.join(lines))
            file_obj.seek(0)
            result_lines = list(read_file_with_filter(file_obj, search_words))

        self.assertEqual(result_lines, ['Vestibulum anTe', 'In faucibus'])

    def test_read_file_with_filter_next_to_file_end_stop_iteration(self):
        """Test StopIteration at the end of file"""
        lines = ['Vestibulum ante', 'ipsum primis', 'in faucibus']
        search_words = None
        with (io.StringIO()) as file_obj:
            file_obj.write(os.linesep.join(lines))
            file_obj.seek(0)
            file_line_generator = read_file_with_filter(file_obj, search_words)

            next(file_line_generator)
            next(file_line_generator)
            next(file_line_generator)
            with self.assertRaises(StopIteration):
                next(file_line_generator)

    def test_read_file_with_filter_empty_file_stop_iteration(self):
        """Test StopIteration when file is empty"""
        with(io.StringIO()) as file_obj:
            file_line_generator = read_file_with_filter(file_obj)
            with self.assertRaises(StopIteration):
                next(file_line_generator)
