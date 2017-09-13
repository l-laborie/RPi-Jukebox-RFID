from jukebox.wrappers import ProcessWrapper


class DummyProcess(object):

    class _DummyStream(object):

        def __init__(self, line=None):
            self.line = line or ''

        def readline(self):
            return self.line

        def write(self, message):
            self.line = message

    def __init__(self):
        stream = DummyProcess._DummyStream()
        self.stdout = stream
        self.stdin = stream

    # pylint: disable=no-self-use
    def poll(self):
        return 0

    def wait(self):
        pass


class DummyProcessWrapper(ProcessWrapper):
    @staticmethod
    def _create_process(args):
        return DummyProcess()


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

    # proc_wrap.write('toto')
    # assert proc_wrap.poll() is None

    # proc_wrap.write('')
    # assert proc_wrap.poll() == 0


# pylint: disable=protected-access
def test_cleanup():
    proc_wrap = DummyProcessWrapper()
    proc_wrap.launch(None)
    assert proc_wrap._process is not None

    proc_wrap.clean_up()
    assert proc_wrap._process is None
