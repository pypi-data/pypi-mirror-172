from ntrprtr.action.ActionBase import ActionBase

class DOSTimeAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        r = ""
        c = self._cnvrtr
        hexValues = _bytes.hex(" ")
        
        endianess = action["endianess"]
        if(endianess == "big"):
            r = c.hexToBin(_bytes.hex()).rjust(16, "0")
        elif(endianess == "little"):
            r = c.hexToBin(c.toLittleEndian(hexValues)).rjust(16, "0")   

        hourBits = [r[i:i + 5] for i in range(0, 5, 5)][0]
        minuteBits = [r[i:i + 6] for i in range(5, 11, 6)][0]
        secondBits = [r[i:i + 5] for i in range(11, 16, 5)][0]

        return str(c.binToDec(hourBits)) + ":" + str(c.binToDec(minuteBits)) + ":" +  str(c.binToDec(secondBits)*2)
