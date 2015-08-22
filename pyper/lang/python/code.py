from pyper.core.code import CodeElement


class Pass(CodeElement):
    """
    The ``pass`` expression.
    """
    def emit(self, source_file):
        source_file.write_line("pass")


class Class(CodeElement):

    def __init__(self, name, base_class="object"):
        self._name = name
        self._base_class = base_class
        self._class_attributes = []
        self._methods = []

    def emit(self, source_file):
        """
        Emits the current code element into the supplied source file.

        :param source_file:
        :type source_file: SourceFile.
        """
        cls_declaration = "class %s(%s):" % (self._name, self._base_class)
        source_file.write_line(cls_declaration)
        with source_file.indented_block():
            if not self._class_attributes and not self._methods:
                # An empty class
                source_file.write_line("pass")

    def add_class_attribute(self, name, value):
        pass

    def add_method(self, method):
        self._methods.append(method)


class Function(CodeElement):

    def __init__(self, name):
        self._name = name

    def emit(self, source_file):
        pass