class player:
    all = []
    chat_id = ''
    def __init__(self, name, id, cards):
        self.name = name
        self.id = id
        self.cards = cards
        player.all.append([self.name, self.id, self.cards])
