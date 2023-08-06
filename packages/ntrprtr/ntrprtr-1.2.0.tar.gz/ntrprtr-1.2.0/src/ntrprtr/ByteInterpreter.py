from cnvrtr.Converter import Converter

from ntrprtr.action.ActionType import ActionType
from ntrprtr.action.DOSDateAction import DOSDateAction
from ntrprtr.action.DOSTimeAction import DOSTimeAction
from ntrprtr.action.DecimalAction import DecimalAction
from ntrprtr.action.AsciiAction import AsciiAction
from ntrprtr.action.BinaryAction import BinaryAction
from ntrprtr.action.EqualsAction import EqualsAction
from ntrprtr.action.HexdumpAction import HexdumpAction

class ByteInterpreter():
    def __init__(self, bytes, config) -> None:
        self._bytes = bytes
        self._config = config
        self._cnvrtr = Converter()
        

    def interpret(self):
        result = []
        for c in self._config:
            b = bytearray()
            amount = c["end"] - c["start"] + 1
            subBytes = [self._bytes[i:i + amount] for i in range(c["start"], c["end"]+1, amount)][0]
            b.extend(subBytes)
            if(c.get("action") != None):
                actionResult = self.__processActions(c["action"], b)
                result.append((c["name"], c["description"], c["action"]["type"], b, actionResult))
            else:
                actionResult = ""
                result.append((c["name"], c["description"], "None", b, actionResult)) 
        return result

    def __processActions(self, action, b):
        result = ""
        type_ = action["type"]
        if(type_ == ActionType.DECIMAL):
            result = DecimalAction().process(action, b)
        elif(type_ == ActionType.ASCII):
            result = AsciiAction().process(action, b)
        elif(type_ == ActionType.EQUALS):
            result = EqualsAction().process(action, b)
        elif(type_ == ActionType.BINARY):
            result = BinaryAction().process(action, b)
        elif(type_ == ActionType.HEXDUMP):
            result = HexdumpAction().process(action, b)
        elif(type_ == ActionType.DOSDATE):
            result = DOSDateAction().process(action, b)
        elif(type_ == ActionType.DOSTIME):
            result = DOSTimeAction().process(action, b)

        return result

    