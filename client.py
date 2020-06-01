from multiprocessing.managers import SyncManager
import classes
import random


class Client(SyncManager):
    results = None
    actions = None
    lock = None

    def __init__(self, address: tuple, password: str):
        super().__init__(address, password.encode('utf-8'))
        self.register('get_actions')
        self.register('get_name')
        self.register('get_results')
        self.register('get_lock')
        self.register('delete_action')

    def connect(self):
        super().connect()
        self.actions = self.get_actions()
        self.results = self.get_results()
        self.lock = self.get_lock()


client = Client(('127.0.0.1', 1234), '123')
client.connect()
print(f'Connected to {client.get_name()}')
while True:
    client.lock.acquire()
    client.lock.wait()
    print('Locked on action !')
    client.delete_action()
    client.results.put(classes.Result(random.randint(0, 100)))
    client.lock.release()
