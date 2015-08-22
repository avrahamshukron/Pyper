from StringIO import StringIO
from unittest import TestCase
from pyper.lang.python.source import PythonSourceFile

__author__ = "avraham.shukron@gmail.com"


class CodeTest(TestCase):
      def check_element_code_emission(self, elem, expected_code):
          stream = StringIO()
          source_file = PythonSourceFile(stream)
          source_file.add_element(elem).emit()
          self.assertEqual(expected_code, stream.getvalue())
          stream.close()