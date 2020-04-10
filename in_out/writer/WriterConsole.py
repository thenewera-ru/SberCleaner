from in_out.writer import Writer as Parent


class WriterConsole(Parent):

    def __init__(self):
        super(WriterConsole, self).__init__()

    def write(self, data, **kwargs):
        print(data)
