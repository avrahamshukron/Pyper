from pyper.core.code import CodeElement


class Pass(CodeElement):
    """
    The ``pass`` expression.
    """
    def emit(self, source_file):
        source_file.write_line("pass")


class Class(CodeElement):

    def __init__(self, name, parents="object"):
        """
        Initializes a new Class object.

        :param name: The class name.
        :type name: str
        :param parents: The name/names of all the super classes of this class.
        :type parents: (tuple | str)
        """
        self._name = name
        self._base_class_names = ((parents,) if isinstance(parents, str)
                                  else parents)
        self._class_attributes = []
        self._methods = []

    def emit(self, source_file):
        """
        Emits the current code element into the supplied source file.

        :param source_file:
        :type source_file: SourceFile.
        """
        parents = ("object" if not self._base_class_names
                   else ", ".join(self._base_class_names))
        cls_declaration = "class %s(%s):" % (self._name, parents)
        source_file.write_line(cls_declaration)
        with source_file.indented_block():
            if not self._class_attributes and not self._methods:
                # An empty class
                source_file.emit_element(Pass())
            for element in self._class_attributes + self._methods:
                source_file.emit_element(element).line_feed()

    def add_class_attribute(self, name, value):
        pass

    def add_method(self, method):
        self._methods.append(method)

    def add_static_method(self, method):
        method.add_decorator(Decorators.STATICMETHOD)
        self.add_method(method)


class Function(CodeElement):

    def __init__(self, name, *args, **kwargs):
        self._name = name
        self.parameters = Parameters(*args, **kwargs)
        self._decorators = []
        self._body = Pass()

    def emit(self, source_file):
        for decorator in self._decorators:
            decorator.emit(source_file)

        source_file.write("def %s" % (self._name,))\
            .emit_element(self.parameters)\
            .write(":")\
            .line_feed()\
            .emit_indented(self._body)

    def add_decorator(self, decorator):
        self._decorators.append(decorator)


class Decorator(CodeElement):

    def __init__(self, name, *args, **kwargs):
        self._name = name
        self.parameters = Parameters(*args, **kwargs)

    def emit(self, source_file):
        source_file.write("@%s" % (self._name, ))
        if self.parameters:
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

    def __init__(self, required_args=None, optional_args=None):
        self.var_args_list = VarArgsList(required_args, optional_args)

    def emit(self, source_file):
        source_file.write("(")\
            .emit_element(self.var_args_list)\
            .write(")")

    def __nonzero__(self):
        return self.var_args_list.__nonzero__()


class IfStatement(CodeElement):

    def __init__(self, condition, positive_block, else_clause=None):
        """
        Initializes a new ``if`` statement.

        :param condition: An expression that can be evaluated as a ``bool``.
        :param positive_block: Code element to execute if ``condition``
            evaluates to ``True``.
        :param else_clause: An ElseStatement instance to be executed if
            ``condition`` evaluates to ``False``.
        """
        self._condition = condition
        self._positive_block = positive_block
        self._else_clause = else_clause

    def emit(self, source_file):
        """
        :param source_file: The source file.
        :type source_file: pyper.core.source.SourceFile
        """
        source_file.write("if ")\
            .emit_element(self._condition)\
            .write(":")\
            .line_feed()\
            .emit_indented(self._positive_block)\
            .line_feed()\
            .emit_element(self._else_clause)


class ElseStatement(CodeElement):

    def __init__(self, code_element, condition=None, else_clause=None):
        """
        Initializes a new Else Statement.

        :param code_element: The code element of the else clause.
        :param condition: An optional boolean expression. If provided, will turn
            the ``else`` into an ``elif`` clause.
        """
        self._code = code_element if code_element is not None else Pass()
        self._condition = condition
        self._else_clause = else_clause

    def emit(self, source_file):
        """
        :type source_file: pyper.core.source.SourceFile
        """
        keyword = "else" if self._condition is None else "elif "
        source_file.write(keyword)\
            .emit_element(self._condition)\
            .write(":")\
            .line_feed()\
            .emit_indented(self._code)\
            .line_feed()\
            .emit_element(self._else_clause)


class Decorators(object):
    STATICMETHOD = Decorator("staticmethod")
    CLASSMETHOD = Decorator("classmethod")
