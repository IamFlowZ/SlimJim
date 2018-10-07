class MessageModel:
    def __init__(self, heading, velocity):
        self.message = {
            'velocity': velocity,
            'heading': heading
        }
