class MessageModel:
    def __init__(self, x, y):
        self.input = {
            'x': x,
            'y': y
        }

        self.output = {
            'prm_mtr': '',
            'prm_mtr_spd': 0,
            'sec_mtr': '',
            'sec_mtr_spd': 0
        }
