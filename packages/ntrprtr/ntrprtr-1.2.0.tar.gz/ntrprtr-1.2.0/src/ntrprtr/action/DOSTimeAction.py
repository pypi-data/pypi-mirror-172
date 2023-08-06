from ntrprtr.action.ActionBase import ActionBase

class DOSTimeAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        hexValues = _bytes.hex(" ")
        r = self._cnvrtr.hexToBin(self._cnvrtr.toLittleEndian(hexValues)).rjust(16, "0")
        b = " ".join(r[i:i+4] for i in range(0, len(r), 4))
                
        hourBits = [r[i:i + 5] for i in range(0, 5, 5)][0]
        minuteBits = [r[i:i + 6] for i in range(5, 11, 6)][0]
        secondBits = [r[i:i + 5] for i in range(11, 16, 5)][0]

        return str(self._cnvrtr.binToDec(hourBits)) + ":" + str(self._cnvrtr.binToDec(minuteBits)) + ":" +  str(self._cnvrtr.binToDec(secondBits)*2)
