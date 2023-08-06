from ntrprtr.action.ActionBase import ActionBase

class EqualsAction(ActionBase):
    def __init__(self):
        super().__init__()

    def process(self, action, _bytes):
        result = action["noMatch"]
        for i in range(0, len(action["cmp"])):
            if(_bytes.hex() == action["cmp"][i]["value"].lower()):
                result = action["cmp"][i]["description"]
        return result