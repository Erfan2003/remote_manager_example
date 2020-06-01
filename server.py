from multiprocessing.managers import SyncManager
from multiprocessing import Manager, Queue, Condition, Lock
import classes
import os


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Server(SyncManager):
    __results = Queue(2)
    lock = Condition(Lock())

    def delete_action(self):
        self.actions = self.actions[1:]

    def __init__(self, name: str, address: tuple, password: str, actions: list):
        self.name = name
        self.actions = actions
        super().__init__(address, password.encode('utf-8'))
        self.register('get_actions', lambda: self.actions)
        self.register('get_name', lambda: self.name)
        self.register('get_results', lambda: self.__results)
        self.register('get_lock', lambda: self.lock)
        self.register('delete_action', self.delete_action)

    def show_results(self, wanted_results):
        for _ in range(wanted_results):
            print(self.__results.get().result)


with Manager() as manager:
    server = Server('Sholex', ('127.0.0.1', 1234), '123', manager.list())
    server.start()
    try:
        while True:
            clear()
            if (user_input := input('Please enter an action name : ')) == 'random':
                new_action = classes.Action('random')
            else:
                continue
            server.actions.extend(tuple([new_action for _ in range(2)]))
            server.lock.acquire(True)
            server.lock.notify_all()
            server.lock.release()
            server.show_results(int(input('How many clients ? : ')))
            input('Done !\nPress Enter to continue !')
    except KeyboardInterrupt:
        server.shutdown()
        clear()
