class UserException:
    class Exceptions(Exception):
        def __init__(self, message):
            super().__init__(message)

    class MissedData(Exceptions):
        def __init__(self, message):
            super().__init__(message)

    class UserExists(Exceptions):
        def __init__(self):
            super().__init__("User already exists")

    class UserNotExists(Exceptions):
        def __init__(self):
            super().__init__("User not exists")

    class BadAuth(Exceptions):
        def __init__(self):
            super().__init__("Invalid auth attempt")
