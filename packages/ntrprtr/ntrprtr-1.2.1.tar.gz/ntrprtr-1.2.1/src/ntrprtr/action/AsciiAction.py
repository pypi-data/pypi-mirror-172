from ntrprtr.action.ActionBase import ActionBase

class AsciiAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        return self._cnvrtr.hexToAsciiString(_bytes.hex())