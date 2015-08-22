from pyper.core.source import SourceFile, FOUR_SPACES


class PythonSourceFile(SourceFile):

    def __init__(self, stream, indentation=FOUR_SPACES, **kwargs):
        SourceFile.__init__(self, stream=stream, indentation=indentation,
                            **kwargs)
