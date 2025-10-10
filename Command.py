import abc
import My_System
from datetime import datetime
import calendar


class Command(abc.ABC):         # абстрактный класс команды
    def __init__(self):         # Инициализация команды
        self.validArgs = []
        self.passedArgs = []

    def execute(self):          # вызов команды
        pass

    def ParseArgs(self, s):     # Парсинг аргументов
        if s not in self.validArgs:
            return -1
        self.passedArgs = s
        return 0

"""Команда CD(перемещение) Аргументы: Путь к директории(относительный или абсолютный)"""
class CDCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        if self.path == "":
            success = self.sys.change_directory("/")
        else:
            success = self.sys.change_directory(self.path)

        if not success:
            print(f"Failed to change directory to: {self.path}")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.path = ""

        for arg in s:
            if arg[0] != "-":
                self.path = arg
            else:
                print(f"Wrong argument: {arg}")
                return -1
        return 0

"""Команда LS(Просмотр директории) Аргументы: Путь к директории(относительный или абсолютный), -a - отображение скрытых файлов(начинающихся на точку)"""
class LSCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-l", "-a"]
        self.passedArgs = []
        self.sys = sys
        self.path = ""

    def execute(self):
        self.sys.list_directory(self.path, self.passedArgs)

    def ParseArgs(self, s):
        self.passedArgs = []
        self.path = ""

        for arg in s:
            if arg[0] != "-":
                self.path = arg
            elif arg in self.validArgs:
                self.passedArgs.append(arg)
            else:
                print(f"Wrong argument: {arg}")
                return -1
        return 0

"""Команда EXIT(Выход из программы)"""
class EXITCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys

    def execute(self):
        print("Exiting emulator...")
        self.sys.exit()

    def ParseArgs(self, s):
        self.passedArgs = []
        if len(s) != 0:
            print("Error: exit command takes no arguments")
            return -1
        return 0

"""Команда, которая отрабатываются при вводе пользователем несуществующей команды"""
class WRONGCommand(Command):
    def __init__(self):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []

    def execute(self):
        print("Error: Wrong command. Available commands: cd, ls, exit, uniq, head, cal, vfs-save, rm")

    def ParseArgs(self, s):
        return 0

"""Команда VFS_SAVE(Сохранение состояния) заглушка"""
class VFS_SAVECommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = []
        self.passedArgs = []
        self.sys = sys
        self.save_path = ""

    def execute(self):

        if self.save_path:
            success = self.sys.save_vfs(self.save_path)
            if success:
                print(f"VFS saved successfully to: {self.save_path}")
            else:
                print(f"Failed to save VFS to: {self.save_path}")
        else:
            print("Error: No save path specified")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.save_path = ""

        if len(s) == 0:
            print("Error: vfs-save requires a path argument")
            return -1

        if len(s) > 1:
            print("Error: vfs-save takes only one argument")
            return -1

        self.save_path = s[0]
        return 0

"""Команда UNIQ(отображает уникальные строки из входных данных) аргументы: -i игнорирование регистра входных данных, -c подсчёт того, сколько раз строка встречается в входных данных
-d отображает только те строки, которые повторяются, -u отображает только уникальные строки"""
class UNIQCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-i", "-c", "-d", "-u"]
        self.passedArgs = []
        self.sys = sys
        self.file_path = ""
        self.input_lines = []

    def execute(self):
        if not self.file_path:
            print("Error: No file specified")
            return

        # Получаем содержимое файла из VFS(генерируются в коде)
        content = self.sys.get_file_content(self.file_path)
        if content is None:
            print(f"Error: Cannot read file '{self.file_path}'")
            return

        lines = content.split('\n')
        result_lines = self._process_uniq(lines)

        for line in result_lines:
            print(line)

    def _process_uniq(self, lines):
        if not lines:
            return []

        result = []
        prev_line = None
        count = 0

        for line in lines:
            compare_line = line.lower() if "-i" in self.passedArgs else line

            if prev_line is None:
                prev_line = compare_line
                count = 1
                continue

            if compare_line == prev_line:
                count += 1
            else:
                self._add_to_result(result, prev_line, count, lines)
                prev_line = compare_line
                count = 1

        if prev_line is not None:
            self._add_to_result(result, prev_line, count, lines)

        return result

    def _add_to_result(self, result, line, count, original_lines):
        if "-c" in self.passedArgs:
            result.append(f"{count:4d} {line}")
        elif "-d" in self.passedArgs and count > 1:
            result.append(line)
        elif "-u" in self.passedArgs and count == 1:
            result.append(line)
        elif not self.passedArgs or ("-d" not in self.passedArgs and "-u" not in self.passedArgs):
            result.append(line)

    def ParseArgs(self, s):
        self.passedArgs = []
        self.file_path = ""

        for arg in s:
            if arg[0] == "-":
                if arg in self.validArgs:
                    self.passedArgs.append(arg)
                else:
                    print(f"Wrong argument: {arg}")
                    return -1
            else:
                if not self.file_path:
                    self.file_path = arg
                else:
                    print(f"Error: Multiple files specified: {arg}")
                    return -1

        if not self.file_path:
            print("Error: No file specified")
            return -1

        return 0

"""Команда HEAD(отображает первые строки входных данных) Аргументы: -n показывает заданное кол-во строк"""
class HEADCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-n"]
        self.passedArgs = []
        self.sys = sys
        self.file_path = ""
        self.line_count = 10  # default value

    def execute(self):
        if not self.file_path:
            print("Error: No file specified")
            return

        # Получаем содержимое файла из VFS(файлы генерируются в коде)
        content = self.sys.get_file_content(self.file_path)
        if content is None:
            print(f"Error: Cannot read file '{self.file_path}'")
            return

        lines = content.split('\n')
        lines_to_show = lines[:self.line_count]

        for i, line in enumerate(lines_to_show, 1):
            print(line)

    def ParseArgs(self, s):
        self.passedArgs = []
        self.file_path = ""
        self.line_count = 10

        i = 0
        while i < len(s):
            arg = s[i]
            if arg == "-n":
                if i + 1 < len(s):
                    try:
                        self.line_count = int(s[i + 1])
                        self.passedArgs.append(arg)
                        i += 1
                    except ValueError:
                        print(f"Error: Invalid number for -n option: {s[i + 1]}")
                        return -1
                else:
                    print("Error: -n option requires a number")
                    return -1
            elif arg[0] == "-":
                print(f"Wrong argument: {arg}")
                return -1
            else:
                if not self.file_path:
                    self.file_path = arg
                else:
                    print(f"Error: Multiple files specified: {arg}")
                    return -1
            i += 1

        if not self.file_path:
            print("Error: No file specified")
            return -1

        return 0


"""Команда CAL(календарь) аргументы Месяц год, -y отображает календарь текущего года, -3 - отображает календарь с предыдущим, текущим и следующим месяцем"""
class CALCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-y", "-3"]
        self.passedArgs = []
        self.sys = sys
        self.month = None
        self.year = None

    def execute(self):
        now = datetime.now()

        if "-y" in self.passedArgs:
            # Показать весь год
            self.year = self.year or now.year
            self._print_year_calendar(self.year)
        elif "-3" in self.passedArgs:
            # Показать предыдущий, текущий и следующий месяц
            self._print_three_months(now)
        else:
            # Показать один месяц
            self.month = self.month or now.month
            self.year = self.year or now.year
            self._print_month_calendar(self.month, self.year)

    def _print_month_calendar(self, month, year):
        print(calendar.month(year, month))

    def _print_year_calendar(self, year):
        print(calendar.calendar(year))

    def _print_three_months(self, now):
        current_month = now.month
        current_year = now.year

        # Предыдущий месяц
        prev_month = current_month - 1
        prev_year = current_year
        if prev_month == 0:
            prev_month = 12
            prev_year = current_year - 1

        # Следующий месяц
        next_month = current_month + 1
        next_year = current_year
        if next_month == 13:
            next_month = 1
            next_year = current_year + 1

        print(f"=== {calendar.month_name[prev_month]} {prev_year} ===")
        print(calendar.month(prev_year, prev_month))

        print(f"=== {calendar.month_name[current_month]} {current_year} ===")
        print(calendar.month(current_year, current_month))

        print(f"=== {calendar.month_name[next_month]} {next_year} ===")
        print(calendar.month(next_year, next_month))

    def ParseArgs(self, s):
        self.passedArgs = []
        self.month = None
        self.year = None

        for arg in s:
            if arg in self.validArgs:
                self.passedArgs.append(arg)
            elif arg[0] == "-":
                print(f"Wrong argument: {arg}")
                return -1
            else:
                try:
                    num = int(arg)
                    if 1 <= num <= 12:
                        if self.month is None:
                            self.month = num
                        else:
                            print(f"Error: Multiple months specified: {arg}")
                            return -1
                    elif 1 <= num <= 9999:
                        if self.year is None:
                            self.year = num
                        else:
                            print(f"Error: Multiple years specified: {arg}")
                            return -1
                    else:
                        print(f"Error: Invalid number: {arg}")
                        return -1
                except ValueError:
                    print(f"Error: Invalid argument: {arg}")
                    return -1

        # Проверка конфликта
        if "-y" in self.passedArgs and self.month is not None:
            print("Error: Cannot specify month with -y option")
            return -1

        return 0

'''Команда RM(удаление) аргументы: -r рекурсивное удаление, -f удаление без предупреждения, -i запрашивание подтверждения '''
class RMCommand(Command):
    def __init__(self, sys: My_System):
        super().__init__()
        self.validArgs = ["-r", "-f", "-i"]
        self.passedArgs = []
        self.sys = sys
        self.paths = []

    def execute(self):
        if not self.paths:
            print("Error: No paths specified")
            return

        for path in self.paths:
            success = self.sys.remove_path(path, self.passedArgs)
            if success:
                print(f"Successfully removed: {path}")
            else:
                print(f"Failed to remove: {path}")

    def ParseArgs(self, s):
        self.passedArgs = []
        self.paths = []

        for arg in s:
            if arg[0] == "-":
                if arg in self.validArgs:
                    self.passedArgs.append(arg)
                else:
                    print(f"Wrong argument: {arg}")
                    return -1
            else:
                self.paths.append(arg)

        if not self.paths:
            print("Error: No paths specified")
            return -1

        return 0