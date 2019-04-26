class TaskException:
    class Exceptions(Exception):
        def __init__(self, message):
            super().__init__(message)

    class MissedData(Exceptions):
        def __init__(self, message):
            super().__init__(message)

    class WrongStatus(Exceptions):
        def __init__(self):
            super().__init__("You try to set nonexistent status")

    class TaskNotExists(Exceptions):
        def __init__(self):
            super().__init__("Task not exists")

    class BadAuth(Exceptions):
        def __init__(self):
            super().__init__("Invalid auth attempt")

    class DataViolation(Exceptions):
        def __init__(self):
            super().__init__("You can change only your deals")