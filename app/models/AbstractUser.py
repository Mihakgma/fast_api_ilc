class AbstractUser:
    __ID = 0

    def __new__(cls, *args, **kwargs):
        cls.__ID += 1
        return super().__new__(cls)

    @classmethod
    def get_id(cls):
        return cls.__ID
