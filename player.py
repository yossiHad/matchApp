class Player:

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket

    def get_socket(self):
        return self.socket

    def get_name(self):
        return self.name