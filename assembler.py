class Assembler:
    def __init__(self):
        self.instructions = {
            "NOOP": 0x0,
            "LDA": 0x1,
            "STA": 0x2,
            "ADD": 0x3,
            "SUB": 0x4,
            "CMP": 0x5,
            "JZ": 0x6,
            "OUT": 0x7,
            "AND": 0x8,
            "OR": 0x9,
            "XOR": 0xA,
            "INC": 0xB,
            "DEC": 0xC,
            "CLEA": 0xD,
            "INP": 0xE,
        }
        self.addressing_modes = {
            "&": 0,  # Непосредственная
            "?": 1,  # Прямая
            "/": 2,  # Регистровая
            "@": 3,  # Косвенно-регистровая
        }
        # Карта символов регистров в индексы
        self.register_map = {
            'A': 0, 'B': 1, 'C': 2, 'D':3,
        }

    def assemble(self, code):
        """Преобразование ассемблерного кода в машинный код с двухпроходной сборкой."""
        labels = {}
        instruction_addresses = []  # храним строки, которые являются инструкциями
        instruction_counter = 0

        # Первый проход
        for index, line in enumerate(code):
            line = line.strip()
            if not line:
                continue

            if ":" in line:
                label, rest = line.split(":", 1)
                label = label.strip()
                rest = rest.strip()
                labels[label] = instruction_counter
                if rest:
                    instruction_addresses.append(rest)
                    instruction_counter += 1
            else:
                instruction_addresses.append(line)
                instruction_counter += 1

        machine_code = []
        for line in instruction_addresses:
            parts = line.split()
            opcode = self.instructions[parts[0]]
            if len(parts) == 1:
                instruction = (opcode << 12)
            else:
                operand = parts[1]
                if operand[0] in self.addressing_modes:
                    addressing_mode_symbol = operand[0]
                    operand_str = operand[1:]
                else:
                    addressing_mode_symbol = '?'
                    operand_str = operand

                addressing_mode = self.addressing_modes[addressing_mode_symbol]

                if operand_str in labels:
                    address = labels[operand_str]
                else:
                    if addressing_mode in (2, 3):  # / или @
                        if operand_str in self.register_map:
                            address = self.register_map[operand_str]
                        else:
                            address = int(operand_str, 16)
                    else:
                        address = int(operand_str, 16)

                instruction = (opcode << 12) | (addressing_mode << 10) | address
            machine_code.append(instruction)

        return machine_code
