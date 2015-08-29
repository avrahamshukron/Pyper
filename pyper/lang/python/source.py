from pyper.core.source import SourceFile


class PythonSourceFile(SourceFile):

    def __init__(self, stream, indentation=SourceFile.FOUR_SPACES, **kwargs):
        SourceFile.__init__(self, stream=stream, indentation=indentation,
                            **kwargs)
