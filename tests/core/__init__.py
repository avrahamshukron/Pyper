from StringIO import StringIO
from unittest import TestCase
from pyper.core import source
from pyper.lang.python.source import PythonSourceFile


class CodeTest(TestCase):
    indentation = source.FOUR_SPACES

    def check_element_code_emission(self, elem, expected_code):
        stream = StringIO()
        source_file = PythonSourceFile(stream, indentation=self.indentation)
        source_file.add_element(elem).emit()
        self.assertEqual(expected_code, stream.getvalue())
        print(expected_code)
        stream.close()
