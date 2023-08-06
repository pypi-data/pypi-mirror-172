from ntrprtr.action.ActionBase import ActionBase

class HexdumpAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        offset_ = 0
        result = self.__createHexHeader()
        splittedBytes = [_bytes[i:i + 16] for i in range(0, len(_bytes), 16)]
        for b_ in splittedBytes:
            result += self.__createHexRow(offset_, b_.hex(" "), b_)
            offset_ += 16  
        return result

    def __createHexHeader(self):
        result = ""
        h = "{:8}   {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2} {:2}    {:16}".format("  Offset", "00", "01", "02", "03", "04", "05",
                                                                                                                            "06", "07", "08", "09", "0A", "0B",
                                                                                                                            "0C", "0D", "0E", "0F", "ASCII")
        result += h + "\n"
        result += ("-"*8) + "   " + ("-"*47) + "    " + ("-"*16) +" \n"
        return result

    def __createHexRow(self, offset, hex_, bytes_):
        formatStr = "{:8}   {:47}    {:16}"
        asc = "".join(chr(v) if (v >= 32 and v <= 126) else "." for v in bytes_)
        r = formatStr.format(offset, hex_.upper(), asc)
        return r + " \n"

