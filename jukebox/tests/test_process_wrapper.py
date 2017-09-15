from jukebox.wrappers import ProcessWrapper
from jukebox.wrappers.process_wrapper import NonBlockingStreamReader


class DummyProcess(object):

    class _DummyStream(object):

        def __init__(self, line=None):
            self.line = line or ''

        def readline(self):
            return self.line

        def write(self, message):
            self.line = message

    def __init__(self, line=None):
        stream = DummyProcess._DummyStream(line)
        self.stdout = stream
        self.stdin = stream

    # pylint: disable=no-self-use
    def poll(self):
        return 0 if self.stdout.readline() == '' else None

    def wait(self):
        pass


class DummyStreamReader(object):
    def __init__(self, stream):
        self._stream = stream

    def readline(self):
        return self._stream.readline()

    def terminate(self):
        pass


class DummyProcessWrapper(ProcessWrapper):
    def __init__(self):
        super(DummyProcessWrapper, self).__init__(
            DummyStreamReader, lambda x: DummyProcess(x))


def test_wait():
    proc_wrap = DummyProcessWrapper()
    proc_wrap.wait()

    proc_wrap.launch(None)
    proc_wrap.wait()
    assert True


def test_poll():
    proc_wrap = DummyProcessWrapper()
    assert proc_wrap.poll() is None

    proc_wrap.launch(None)
    assert proc_wrap.poll() == 0

    proc_wrap.launch('_')
    proc_wrap.write('toto')
    assert proc_wrap.poll() is None

    proc_wrap.write('')
    assert proc_wrap.poll() == 0


# pylint: disable=protected-access
def test_cleanup():
    proc_wrap = DummyProcessWrapper()
    proc_wrap.launch(None)
    assert proc_wrap._process is not None

    proc_wrap.clean_up()
    assert proc_wrap._process is None


def test_non_blocking_stream_reader():
    class DummyStream(object):
        def __init__(self):
            self.data = [1, 2, 3]

        def readline(self):
            return self.data.pop() if self.data else None

    stream = NonBlockingStreamReader(DummyStream())
    line = None
    while line is None:
        line = stream.readline()
    assert line == 3
    line = None
    while line is None:
        line = stream.readline()
    assert line == 2
    line = None
    while line is None:
        line = stream.readline()
    assert line == 1
    assert stream.readline() is None
    stream.terminate()
    assert stream.readline() is None
