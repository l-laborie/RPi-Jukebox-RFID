from jukebox.players import Player


class DummyPlayer(Player):
    def __init__(self):
        self.result = ''
        super(DummyPlayer, self).__init__(media_lister=None)

    def process_cleanup(self):
        self.result += 'clean_up '

    def process_decrease_volume(self, *args):
        self.result += 'vol - '

    def process_increase_volume(self, *args):
        self.result += 'vol + '

    def process_is_state_change(self):
        self.result += 'is state change '

    def process_play(self, *args):
        self.result += 'play %r ' % args

    def process_stop(self, *args):
        self.result += 'stop '

    def process_quit(self, *args):
        self.result += 'quit '

    class DummyLogger(object):
        # pylint: disable=no-self-use
        def log(self, level, message):
            print '[%r] %s' % (level, message)

    _logger = DummyLogger()
