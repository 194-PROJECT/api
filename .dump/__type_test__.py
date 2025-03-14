from typing import Optional


class Test[T]:
    data: Optional[T]
        
    def __init__ (self, data: Optional[T] = None):
        self.data = data

    def get_type(self) -> type:
        return self.__orig_class__.__args__[0]

    def validate_data(self) -> bool:
        if isinstance(self.data, self.get_type()):
            return True
        return False

if __name__ == "__main__":
    print(Test[int](data=1).validate_data())
    print(Test[str](data=None).validate_data())
    print(Test[None](data=None).validate_data())