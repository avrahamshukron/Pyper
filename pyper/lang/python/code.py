from pyper.core.code import CodeElement


class Pass(CodeElement):
    """
    The ``pass`` expression.
    """
    def emit(self, source_file):
        source_file.write_line("pass")


class ContainerCodeElement(CodeElement):

    def __init__(self, body=None):
        self._elements = []
        if body is not None:
            self._elements.append(body)

    def emit_header(self, source_file):
        """
        Emits the header of the code element.
        The header is the first line before the indented body.
        Every container code element in Python have a header, so this method
        must be implemented.

        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile.
        """
        raise NotImplementedError("Subclasses must implement")

    def emit(self, source_file):
        """
        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile.
        """
        self.emit_header(source_file)
        self.emit_body(source_file)
        self.emit_footer(source_file)

    def emit_body(self, source_file):
        """
        Emits the body of this element. The body is indented one level relative
        to the header and footer.

        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile.
        """
        if not self._elements:
            self._elements.append(Pass())

        with source_file.indented_block():
            for element in self._elements:
                element.emit(source_file)

        if not source_file.is_new_line():
            source_file.line_feed()

    def emit_footer(self, source_file):
        """
        Emits the finishing part of the code element.
        Called after ``emit_body``.

        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile.
        """
        pass


class Class(ContainerCodeElement):

    OBJECT = "object"

    def __init__(self, name, parents=OBJECT):
        """
        Initializes a new Class object.

        :param name: The class name.
        :type name: str
        :param parents: The name/names of all the super classes of this class.
        :type parents: (tuple | str)
        """
        ContainerCodeElement.__init__(self, body=None)
        self._name = name
        self._base_class_names = ((parents,) if isinstance(parents, str)
                                  else parents)

    def emit_header(self, source_file):
        parents = ", ".join(self._base_class_names)
        cls_declaration = "class %s(%s):" % (self._name, parents)
        source_file.write_line(cls_declaration)
        if self._elements:
            source_file.line_feed()

    def add_method(self, method):
        self._elements.append(method)

    def add_static_method(self, method):
        method.add_decorator(Decorators.STATICMETHOD)
        self.add_method(method)


class FunctionDeclaration(ContainerCodeElement):

    def __init__(self, name, parameters=None, body=None):
        ContainerCodeElement.__init__(self, body=body)
        self._name = name
        self._parameters = (parameters
                            if parameters is not None
                            else Parameters())
        self._decorators = []

    def emit_header(self, source_file):
        for decorator in self._decorators:
            decorator.emit(source_file)

        source_file.write("def %s" % (self._name,))\
            .emit_element(self._parameters)\
            .write(":")\
            .line_feed()

    def add_decorator(self, decorator):
        self._decorators.append(decorator)


class Decorator(CodeElement):

    def __init__(self, name, parameters=None):
        self._name = name
        self.parameters = parameters

    def emit(self, source_file):
        source_file.write("@%s" % (self._name, ))
        if self.parameters is not None:
            self.parameters.emit(source_file)
        source_file.line_feed()


class VarArgsList(CodeElement):
    """
    Corresponds to the varargslist grammar variable of Python
    """
    def __init__(self, required_args=None, optional_args=None):
        """
        Initializes a VarArgsList.

        :param required_args: A tuple of positional argument names.
        :param optional_args: A tuple of (name, default_value) pairs.
        """
        self._positional_args = required_args
        self._optional_args = optional_args

    def emit(self, source_file):
        positional = (", ".join(str(arg) for arg in self._positional_args)
                      if self._positional_args else "")
        kw = (", ".join("%s=%s" % (name, value)
                        for name, value in self._optional_args)
              if self._optional_args else "")
        args_list = ", ".join(l for l in (positional, kw) if l)
        source_file.write(args_list)

    def __nonzero__(self):
        return bool(self._positional_args) or bool(self._optional_args)


class Parameters(CodeElement):

    def __init__(self, positional_args=None, named_args=None):
        self.var_args_list = VarArgsList(positional_args, named_args)

    def emit(self, source_file):
        source_file.write("(")\
            .emit_element(self.var_args_list)\
            .write(")")

    def __nonzero__(self):
        return self.var_args_list.__nonzero__()


class ConditionedCodeElement(ContainerCodeElement):

    KEYWORD = None

    def __init__(self, condition, body, alternative=None):
        """
        Initializes a new ``if`` statement.

        :param condition: An expression that can be evaluated as a ``bool``.
        :param body: Code element to execute if ``condition`` evaluates to
            ``True``.
        :param alternative: An (ElseStatement | ElifStatement) instance.
        :type alternative: ElseStatement | ElifStatement
        """
        ContainerCodeElement.__init__(self, body)
        self._condition = condition
        self._alternative = alternative

    def emit_header(self, source_file):
        """
        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile
        """
        source_file.write("%s " % (self.KEYWORD,))\
            .emit_element(self._condition)\
            .write(":")\
            .line_feed()

    def emit_footer(self, source_file):
        if self._alternative is not None:
            self._alternative.emit(source_file)


class ElifStatement(ConditionedCodeElement):
    KEYWORD = "elif"


class IfStatement(ConditionedCodeElement):
    KEYWORD = "if"


class ElseStatement(ContainerCodeElement):

    ELSE = "else"

    def emit_header(self, source_file):
        """
        :type source_file: pyper.core.source.SourceFile
        """
        source_file.write(self.ELSE).write(":").line_feed()


class WhileStatement(CodeElement):

    def __init__(self, condition, body):
        self._condition = condition
        self._body = body if body is not None else Pass()

    def emit(self, source_file):
        source_file.write("while ")\
            .emit_element(self._condition)\
            .write(":")\
            .line_feed()\
            .emit_indented(self._body)\
            .line_feed()


class StringLiteral(CodeElement):

    def __init__(self, value):
        self._value = value

    def emit(self, source_file):
        source_file.write("\"%s\"", self._value)


class Decorators(object):
    STATICMETHOD = Decorator("staticmethod")
    CLASSMETHOD = Decorator("classmethod")
