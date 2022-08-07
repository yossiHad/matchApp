class Player:

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket
        self.in_chat = False
        self.game = ""

    def get_socket(self):
        return self.socket

    def get_name(self):
        return self.name

    def is_in_chat(self):
        return self.in_chat

    def set_in_chat(self, in_chat):
        self.in_chat = in_chat

    def set_game(self, game):
        self.game = game

    def reset_game(self):
        self.game = ""
