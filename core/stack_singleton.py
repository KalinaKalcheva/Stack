from core.stack import Stack


class StackSingleton(Stack):
    __instance = None

    @staticmethod
    def get_instance():
        if StackSingleton.__instance is None:
            StackSingleton()
        return StackSingleton.__instance

    def __init__(self):
        if StackSingleton.__instance is None:
            StackSingleton.__instance = super().__init__()
        else:
            raise Exception("Singleton already initialized")
