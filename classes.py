class Action:
    def __init__(self, name: str):
        self.name = name

    def do(self):
        print(f'{self.name} is done !')


class Result:
    def __init__(self, result: str):
        self.result = result
