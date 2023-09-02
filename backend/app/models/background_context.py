class BackgroundContext:

    def __init__(self, strategy=None):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def search_for_background(self, data):
        description = self.strategy.get_background_information(data)
        return {
            'id': data['background'].id,
            'name': data['background'].name,
            'type': data['background'].type,
            'information': description
        }