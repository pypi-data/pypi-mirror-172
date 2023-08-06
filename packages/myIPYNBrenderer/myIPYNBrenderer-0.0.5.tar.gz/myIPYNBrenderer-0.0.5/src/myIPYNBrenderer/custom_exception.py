class InvalidURLException(Exception):
    def __init__(self, message: str="URL is not valied"):
        self.message = message
        super().__init__(self.message)