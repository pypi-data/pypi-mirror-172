from ntrprtr.action.ActionBase import ActionBase

class BinaryAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        result = ""

        endianess = action["endianess"]
        if(endianess == "big"):
            result = self._cnvrtr.hexToBin(_bytes.hex())
        elif(endianess == "little"):
            result = self.__hexToLittleEndianToBin(_bytes)
        
        # Always fill up zeros to represent all given bytes, even if 
        # they are zero
        result = result.rjust(len(_bytes)*8, "0")
        # For better readability add a space after 4 bit
        result = " ".join(result[i:i+4] for i in range(0, len(result), 4))
        return result

    def __hexToLittleEndianToBin(self, byteArr):
        le = self._cnvrtr.toLittleEndian(byteArr.hex(" "))
        return str(self._cnvrtr.hexToBin(le))