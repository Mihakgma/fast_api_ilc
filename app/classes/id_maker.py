class IdMaker:
    __classes_processed = dict()

    def __new__(cls, *args, **kwargs):
        # cannot create an object of the current class
        if cls == IdMaker:
            return
        return super().__new__(cls)

    @staticmethod
    def get_id(class_name: str) -> int:
        if type(class_name) is not str:
            raise TypeError('class_name is not a string')
        if class_name not in IdMaker.__classes_processed:
            IdMaker.__classes_processed[class_name] = 1
        elif class_name in IdMaker.__classes_processed:
            IdMaker.__classes_processed[class_name] += 1
        return IdMaker.__classes_processed[class_name]
