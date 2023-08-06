class Calculator:
    """

    Simple Calculator with memory class.

    Functions:
    1. add;
    2. subtract;
    3. multiply;
    4. divide;
    5. take (n) root;
    6. reset memory.

    """

    def __init__(self, memory: float = 0):
        self.__memory = memory

    def add(self, n: float):
        self.__memory += n

    def subtract(self, n: float):
        self.__memory -= n

    def multiply(self, n: float):
        self.__memory *= n

    def divide(self, n: float):
        self.__memory /= n

    def root(self, n: float = 2):
        self.__memory = self.memory() ** (1/n)

    def reset(self, n: float = 0):
        self.__memory = n

    def memory(self) -> float:
        return self.__memory


if __name__ == "__main__":
    print('Calculator module')
