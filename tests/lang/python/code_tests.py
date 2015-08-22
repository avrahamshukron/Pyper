from pyper.lang.python.code import Class
from tests.core import CodeTest


class PythonCodeTest(CodeTest):

    EMPTY_CLASS_TEMPLATE = "class %s(%s):\n    pass\n"

    def test_class(self):
        class_name = "TestClass"
        cls = Class(class_name)
        expected = self.EMPTY_CLASS_TEMPLATE % (class_name, "object")
        self.check_element_code_emission(cls, expected)

    def test_class_with_base_class(self):
        class_name = "TestClass"
        base_class_name = "MyBaseClass"
        cls = Class(class_name, base_class_name)
        expected = self.EMPTY_CLASS_TEMPLATE % (class_name, base_class_name)
        self.check_element_code_emission(cls, expected)
