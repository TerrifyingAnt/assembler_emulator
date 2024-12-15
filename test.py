import io
import sys
from cpu import CPU
from assembler import Assembler

def run_program(cpu, assembler, program_code):
    # Загрузка скомпилированной программы в память команд
    cpu.instruction_memory[:len(program_code)] = program_code
    # Перенаправим stdout для перехвата вывода OUT
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output

    cpu.run()

    # Возвращаем stdout обратно
    sys.stdout = old_stdout
    # Получаем вывод
    output = redirected_output.getvalue().strip()
    return output

def test_from_file(filename, expected_output):
    cpu = CPU(memory_size=1024)
    assembler = Assembler()

    # Инициализируем память так, как было показано в примере
    cpu.memory[0] = 5   # Размер массива
    cpu.memory[1] = 10  # Адрес первого элемента массива
    cpu.memory[10] = 2
    cpu.memory[11] = 3
    cpu.memory[12] = 4
    cpu.memory[13] = 5
    cpu.memory[14] = 6

    # Считываем программу из файла
    with open(filename, "r", encoding="utf-8") as f:
        program = []
        for line in f:
            line = line.strip()
            if line and not line.startswith(";"):
                program.append(line)

    program_code = assembler.assemble(program)
    output = run_program(cpu, assembler, program_code)

    print(f"Test from file {filename}:")
    print(f"Expected: {expected_output}, Got: {output}")
    print("Passed" if expected_output in output else "Failed")

def test_from_lines(program_lines, expected_output):
    cpu = CPU(memory_size=1024)
    assembler = Assembler()

    # Инициализация памяти
    cpu.memory[0] = 5   # Размер массива
    cpu.memory[1] = 10  # Адрес первого элемента массива
    cpu.memory[10] = 2
    cpu.memory[11] = 3
    cpu.memory[12] = 4
    cpu.memory[13] = 5
    cpu.memory[14] = 6

    program_code = assembler.assemble(program_lines)
    output = run_program(cpu, assembler, program_code)

    print("Test from lines:")
    print(f"Expected: {expected_output}, Got: {output}")
    print("Passed" if expected_output in output else "Failed")

if __name__ == "__main__":
    expected_file_output = "Output: 20"
    test_from_file("array_sum.asm", expected_file_output)

    # Тест из строк
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
    expected_lines_output = "Output: 20"
    test_from_lines(program, expected_lines_output)
