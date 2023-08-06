from ntrprtr.action.ActionBase import ActionBase

class DecimalAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        result = ""
        endianess = action["endianess"]
        if(endianess == "big"):
            result = self._cnvrtr.hexToDec(_bytes.hex())
        elif(endianess == "little"):
            result = self.__hexToLittleEndianToDec(_bytes)
        return result

    def __hexToLittleEndianToDec(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return str(self._cnvrtr.hexToDec(le))