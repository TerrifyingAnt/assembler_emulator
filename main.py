from cpu import CPU
from assembler import Assembler

cpu = CPU(memory_size=1024)
assembler = Assembler()

# Запись массива в память
cpu.memory[0] = 6   # Размер массива
cpu.memory[1] = 10  # Адрес первого элемента массива
cpu.memory[10] = 2 # Элементы массива
cpu.memory[11] = 3
cpu.memory[12] = 4
cpu.memory[13] = 5
cpu.memory[14] = 6
cpu.memory[15] = 7

program = [
    "STA /B",
    "LDA ?1", # Загрузка в аккум значения из памяти
    "STA /C", # Сохранение значения из аккума в регистр -> адрес
    "LDA @C",
    "LOOP123: ADD /A",
        "STA /A",
        "LDA /C",
        "INC /C",
        "STA /C",
        "LDA /B",
        "INC /B",
        "STA /B",
        "CMP ?0",
        "LDA @C",
    "JZ LOOP123",
    "LDA /A",
    "OUT"
]

program_code = assembler.assemble(program)
#print(program_code)
cpu.instruction_memory[:len(program_code)] = program_code
cpu.run()

