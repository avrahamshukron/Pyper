from cStringIO import StringIO
import unittest
from pyper.core.code import CodeElement, TextCodeElement
from pyper.core.source import SourceFile
from tests.core import CodeTest


class SourceFileTest(unittest.TestCase):

    def test_emit_indented(self):
        output_stream = StringIO()
        s = SourceFile(output_stream, indentation=SourceFile.TAB)
        hello = "hello"
        expected = SourceFile.TAB + hello
        s.emit_indented(TextCodeElement(hello))
        self.assertEqual(output_stream.getvalue(), expected)
        output_stream.close()


class CoreCodeTest(CodeTest):

    def test_code_element_is_abstract(self):
        element = CodeElement()
        self.assertRaises(NotImplementedError, element.emit, None)

    def test_text_code_element(self):
        expected = "hello\nworld\nfoo\nbar"
        text = TextCodeElement(initial_value="hello")
        text.add_line("world")
        text.add_line("foo")
        text.add_line("bar")
        self.check_element_code_emission(text, expected)
