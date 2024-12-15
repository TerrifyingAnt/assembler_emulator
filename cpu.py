class CPU:
    def __init__(self, registers_count=8, memory_size=256):
        self.debug = False
        self.registers = [0] * registers_count  # Регистр общего назначения
        self.acc = 0  # Аккумулятор
        self.pc = 0  # Счётчик команд
        self.flag_zero = False  # Флаг ZF (нулевой флаг)
        self.memory = [0] * memory_size  # ОЗУ для данных
        self.instruction_memory = [0] * memory_size  # ПЗУ для команд

    def fetch(self):
        """Извлечение команды из ПЗУ."""
        if self.pc >= len(self.instruction_memory):
            raise IndexError("Превышен размер памяти команд")
        instruction = self.instruction_memory[self.pc]
        self.pc += 1
        return instruction

    def decode(self, instruction):
        """Декодирование команды."""
        opcode = (instruction >> 12) & 0xF  # Первые 4 бита - код операции
        addressing_mode = (instruction >> 10) & 0x3  # Следующие 2 бита - тип адресации
        address = instruction & 0x3FF  # Остальные 10 бит - адрес
        return opcode, addressing_mode, address

    def execute(self, opcode, addressing_mode, address):
        """Исполнение команды."""
        value = self.get_value(addressing_mode, address)
        if opcode == 0:  # NOOP
            pass
        elif opcode == 1:  # LDA - загрузка в аккумулятор
            if (self.debug):
                print(f"Грузим в аккум значение; {value=}")
            self.acc = value
        elif opcode == 2:  # STA - сохранение из аккумулятора в память
            if (self.debug):
                print(f"Сохраняем из аккумулятора в память; {addressing_mode=}; {address=}, значение={self.acc}")
            self.set_value(addressing_mode, address, self.acc)
        elif opcode == 3:  # ADD - сложение
            if (self.debug):
                print(f"Складываем аккум со значением; new_val={self.acc + value}, prev_val={self.acc}")
            self.acc += value
            self.update_flags()
        elif opcode == 4:  # SUB - вычитание
            if (self.debug):
                print(f"{opcode=};")
            self.acc -= value
            self.update_flags()
        elif opcode == 5:  # CMP - сравнение
            if (self.debug):
                print(f"Сравниваем {self.acc=} и {value=}")
            self.flag_zero = (self.acc != value)
        elif opcode == 6:  # JZ - переход, если ZF = 1
            if self.flag_zero:
                self.pc = address
                if (self.debug):
                    print(f"Переходим {address=}")
            else:
                if (self.debug):
                    print(f"Не переходим")  

        elif opcode == 7:  # OUT - вывод аккумулятора
            print("Output:", self.acc, "\n\n")
        elif opcode == 8:  # AND - битовая конъюнкция
            self.acc &= value
            self.update_flags()
        elif opcode == 9:  # OR - битовая дизъюнкция
            self.acc |= value
            self.update_flags()
        elif opcode == 10:  # XOR - исключающее ИЛИ
            self.acc ^= value
            self.update_flags()
        elif opcode == 11:  # INC - инкремент
            if (self.debug):
                print(f"Инкрементируем, старое значение={self.acc}, новое значение={self.acc+1}")
            self.acc += 1
            self.update_flags()
        elif opcode == 12:  # DEC - декремент
            if (self.debug):
                print(f"Декрементируем, старое значение={self.acc}, новое значение={self.acc-1}")
            self.acc -= 1
            self.update_flags()
        elif opcode == 13:  # CLEA - очистка аккумулятора
            if (self.debug):
                print(f"Чистим аккум;")
            self.acc = 0
            self.update_flags()
        elif opcode == 14:  # INP - ввод значения в аккумулятор
            if (self.debug):
                print(f"{opcode=};")
            self.acc = int(input("Enter value: "))
            self.update_flags()
        else:
            raise ValueError(f"Неизвестная команда: {opcode}")

    def get_value(self, addressing_mode, address):
        """Получение значения в зависимости от типа адресации."""
        if addressing_mode == 0:  # Непосредственная
            return address
        elif addressing_mode == 1:  # Прямая
            return self.memory[address]
        elif addressing_mode == 2:  # Регистровая
            return self.registers[address]
        elif addressing_mode == 3:  # Косвенно-регистровая
            indirect_address = self.registers[address]
            return self.memory[indirect_address]
        else:
            raise ValueError(f"Неизвестный тип адресации: {addressing_mode}")

    def set_value(self, addressing_mode, address, value):
        """Установка значения в зависимости от типа адресации."""
        if addressing_mode == 1:  # Прямая
            self.memory[address] = value
        elif addressing_mode == 2:  # Регистровая
            self.registers[address] = value
        elif addressing_mode == 3:  # Косвенно-регистровая
            indirect_address = self.registers[address]
            self.memory[indirect_address] = value
        else:
            raise ValueError(f"Некорректный тип адресации для записи: {addressing_mode}")

    def update_flags(self):
        """Обновление флагов в зависимости от значения аккумулятора."""
        self.flag_zero = (self.acc == 0)

    def run(self):
        """Цикл выполнения команд."""
        while self.pc < len(self.instruction_memory):
            instruction = self.fetch()
            opcode, addressing_mode, address = self.decode(instruction)
            self.execute(opcode, addressing_mode, address)
