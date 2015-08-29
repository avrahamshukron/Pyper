from pyper.core.code import TextCodeElement
from pyper.lang.python.code import Class, Decorator, Parameters, IfStatement, \
    ElseStatement, ElifStatement
from tests.core import CodeTest


class PythonCodeTest(CodeTest):

    EMPTY_CLASS_TEMPLATE = "class %s(%s):\n    pass\n\n"

    def test_class_default_parent(self):
        class_name = "TestClass"
        cls = Class(class_name)
        expected = self.EMPTY_CLASS_TEMPLATE % (class_name, "object")
        self.check_element_code_emission(cls, expected)

    def test_class_single_parent(self):
        class_name = "TestClass"
        parent = "BaseClass"
        cls = Class(class_name, parent)
        expected = self.EMPTY_CLASS_TEMPLATE % (class_name, parent)
        self.check_element_code_emission(cls, expected)

    def test_class_multiple_inheritance(self):
        class_name = "TestClass"
        parents = ("Foo", "Bar", "Baz")
        cls = Class(class_name, parents)
        expected = self.EMPTY_CLASS_TEMPLATE % (class_name, ", ".join(parents))
        self.check_element_code_emission(cls, expected)

    def test_decorator(self):
        name = "deco"
        expected = "@%s\n" % (name,)
        decorator = Decorator(name)
        self.check_element_code_emission(decorator, expected)

    def test_positional_parameters(self):
        params = Parameters(required_args=("a", "b"))
        self.check_element_code_emission(params, "(a, b)")

    def test_keyword_parameters(self):
        params = Parameters(optional_args=(("a", 1), ("b", 2)))
        self.check_element_code_emission(params, "(a=1, b=2)")

    def test_empty_parameters(self):
        params = Parameters()
        self.check_element_code_emission(params, "()")

    def test_full_parameters(self):
        params = Parameters(required_args=("a", "b"),
                            optional_args=(("a", 1), ("b", 2)))
        self.check_element_code_emission(params, "(a, b, a=1, b=2)")

    def test_simple_if_statement(self):
        if_statement = IfStatement(
            condition=TextCodeElement("True and False"),
            body=TextCodeElement("print 'hello'")
        )
        expected = "if True and False:\n    print 'hello'\n"
        self.check_element_code_emission(if_statement, expected)

    def test_else_statement(self):
        else_code = "print 'This is else'"
        if_statement = ElseStatement(
            TextCodeElement(else_code)
        )
        expected = "else:\n%s%s\n" % (self.indentation, else_code)
        self.check_element_code_emission(if_statement, expected)

    def test_elif_statement(self):
        body = "print 'This is elif'"
        condition = "True or False"
        statement = ElifStatement(
            condition=TextCodeElement(condition),
            body=TextCodeElement(body)
        )
        expected = "elif %s:\n%s%s\n" % (condition, self.indentation, body)
        self.check_element_code_emission(statement, expected)

    def test_if_elif_else_statement(self):
        if_body = "print 'This is if'"
        elif_code = "print 'This is elif'"
        else_code = "print 'This is else'"
        condition = "True or False"

        statement = IfStatement(
            condition=TextCodeElement(condition),
            body=TextCodeElement(if_body),
            alternative=ElifStatement(
                body=TextCodeElement(elif_code),
                condition=TextCodeElement(condition),
                alternative=ElseStatement(
                    TextCodeElement(else_code)
                )
            )
        )
        expected = ("if %s:\n"
                    "%s%s\n"
                    "elif %s:\n"
                    "%s%s\n"
                    "else:\n"
                    "%s%s\n") % (
                       condition,
                       self.indentation,
                       if_body,
                       condition,
                       self.indentation,
                       elif_code,
                       self.indentation,
                       else_code
                   )
        self.check_element_code_emission(statement, expected)
