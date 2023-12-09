class CPU:
    def __init__(self):
        self._stack_ = []
        self._lines_ = []
        self._bus_length_ = 24

        self._pc_ = 0
        self._stack_pointer_ = -1
        self._delay_ = 0

        self._zf_ = 0
        self._pf_ = 0

        self._registers = [0 for _ in range(8)]

        self._register_mapping_ = {
            "reg_a": 0,
            "reg_b": 1,
            "reg_c": 2,
            "reg_d": 3,
            "reg_e": 4,
            "reg_f": 5,
            "reg_g": 6,
            "reg_h": 7,
        }

        self._command_mapping_ = {
            "push": self.push,
            "pop": self.pop,
            "add": self.add,
            "sub": self.sub,
            "inc": self.inc,
            "dec": self.dec,
            "imul": self.imul,
            "idiv": self.idiv,
            "and": self.and_operation,
            "or": self.or_operation,
            "xor": self.xor,
            "shl": self.shl,
            "shr": self.shr,
            "cmp": self.cmp,
            "je": self.je,
            "jma": self.jma,
            "jne": self.jne,
            "skip": self.skip
        }

    @property
    def mapping(self) -> dict:
        return self._command_mapping_

    def execute(self, operation: str, *arguments) -> None:
        self._command_mapping_.get(operation)(*arguments)

    def run(self, lines: list[str, ...]) -> None:
        self._lines_ = lines

        while self._pc_ < len(lines):
            self.execute(*lines[self._pc_])

            self._pc_ += 1

    def get_register(self, register: str) -> int:
        return self._registers[self._register_mapping_.get(register)]

    def info(self) -> None:
        print("\nStack\n")

        for index, value in enumerate(self._stack_):
            print(f"{index}: {value}")

        print("\nRegisters\n")

        for index, value in enumerate(self._registers):
            print(f"Register {index}: {value}")

    def push(self, value: str = None) -> None:
        if value:
            if value.replace("-", "").isnumeric():
                self._stack_.append(int(value))
            else:
                raise Exception("Incorrect value")
        else:
            self._stack_.append(self._registers[0])

            self._registers.pop(0)
            self._registers.append(0)

        self._stack_pointer_ += 1

    def pop(self) -> None:
        self._registers = [self._stack_.pop(self._stack_pointer_)] + self._registers[:-1]

        self._stack_pointer_ -= 1
        
    def _pop_(self) -> None:
        self._stack_.pop(-1)
        self._stack_pointer_ -= 1

    def add(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) + self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] += self._stack_[self._stack_pointer_]

        self._pop_()

    def sub(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) - self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] -= self._stack_[self._stack_pointer_]

        self._pop_()

    def inc(self, first: str = None) -> None:
        if first:
            self._registers[self._register_mapping_.get(first)] = self.get_register(first) + 1

            return
        self._stack_[self._stack_pointer_] += 1

    def dec(self, first: str = None) -> None:
        if first:
            self._registers[self._register_mapping_.get(first)] = self.get_register(first) - 1

            return
        self._stack_[self._stack_pointer_] -= 1

    def imul(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) * self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] *= self._stack_[self._stack_pointer_]

        self._pop_()

    def idiv(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) // self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] //= self._stack_[self._stack_pointer_]

        self._pop_()

    def and_operation(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) & self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] &= self._stack_[self._stack_pointer_]

        self._pop_()

    def or_operation(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) | self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] |= self._stack_[self._stack_pointer_]

        self._pop_()

    def shl(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) << self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] = self._stack_[self._stack_pointer_ - 1] << self._stack_[
            self._stack_pointer_]

        self._pop_()

    def shr(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) >> self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] = self._stack_[self._stack_pointer_ - 1] >> self._stack_[
            self._stack_pointer_]

        self._pop_()

    def xor(self, first: str = None, second: str = None, destination: str = None) -> None:
        if all((first, second, destination)):
            self._registers[self._register_mapping_.get(destination)] = self.get_register(first) ^ self.get_register(second)

            return
        elif any((first, second, destination)):
            raise Exception("One of arguments unfilled")

        self._stack_[self._stack_pointer_ - 1] ^= self._stack_[self._stack_pointer_]

        self._pop_()

    def cmp(self, first: str = None, second: str = None) -> None:
        if all((first, second)):
            self._zf_ = int((self.get_register(first) - self.get_register(second)) == 0)
            self._pf_ = int((self.get_register(first) - self.get_register(second)) > 0)

            return
        elif any((first, second)):
            raise Exception("One of arguments unfilled")

        self._zf_ = int((self._stack_[self._stack_pointer_ - 1] - self._stack_[self._stack_pointer_]) == 0)
        self._pf_ = int((self._stack_[self._stack_pointer_ - 1] - self._stack_[self._stack_pointer_]) > 0)

    def je(self, value: str) -> None:
        if (self._pc_ + self._stack_[self._stack_pointer_] not in range(len(self._lines_))) and not value:
            raise Exception("Jump value out of bounds")

        if value:
            if self._zf_:
                self._pc_ = int(value) - 2

                return
        else:
            if self._zf_:
                self._pc_ += self._stack_[self._stack_pointer_]

            self._pop_()

    def jma(self, value: str) -> None:
        if (self._pc_ + self._stack_[self._stack_pointer_] not in range(len(self._lines_))) and not value:
            raise Exception("Jump value out of bounds")

        if value:
            if not self._zf_:
                self._pc_ = int(value) - 2

                return
        else:
            if not self._zf_:
                self._pc_ += self._stack_[self._stack_pointer_]

            self._pop_()

    def jne(self, value: str) -> None:
        if self._stack_:
            if (self._pc_ + self._stack_[self._stack_pointer_] not in range(len(self._lines_))) and not value:
                raise Exception("Jump value out of bounds")

        if value:
            if not self._zf_:
                self._pc_ = int(value) - 2

                return
        else:
            if not self._zf_:
                self._pc_ += self._stack_[self._stack_pointer_]

            self._pop_()

    def skip(self) -> None:
        pass


class Simulator:
    def __init__(self):
        self._CPU_ = CPU()

        self._lines_ = []

    def preprocess(self, path: str) -> None:
        with open(path, "r") as file:
            for index, line in enumerate(file.readlines()):
                if line[0] == ";" or line[0] == "\n":
                    self._lines_.append(["skip"])

                    continue

                splitted = " ".join(line.split()).split(" ")

                command = splitted[0]

                if command not in self._CPU_.mapping:
                    raise Exception("Unknown command")

                self._lines_.append(splitted)

    def run(self, path: str, info: bool = True) -> None:
        self.preprocess(path)

        self._CPU_.run(self._lines_)

        if info:
            self.info()

    def info(self) -> None:
        self._CPU_.info()


def main():
    simulator = Simulator()

    simulator.run("program.txt")


if __name__ == '__main__':
    main()
