# (16 Вариант) Отчёт по реализации эмулятора командной оболочки
## Этап 1 REPL

### Реализованный функционал

1. **Консольный интерфейс**: Создан интерактивный интерфейс командной строки
2. **Приглашение ко вводу**: Реализовано в формате `username@hostname:`
3. **Парсер с поддержкой глобальных переменных**
4. **Обработка ошибок**: Сообщения об неизвестных командах и неверных аргументах
5. **Базовые команды**: Реализованы команды `ls`, `cd` (заглушки) и `exit`

### Примеры

#### Приглашение на ввод
```bash
Alex@Laptop:
```

#### Обработка аргументов
```bash
Alex@MYLAPTOP:cd /home -c -d
i am ls
path is Correct
Arguments ['-c', '-d']
```

#### Неизвестная команда

```bash
Alex@MYLAPTOP:Wrongcommand
Wrong command
```

#### Неизвестные аргументы
```bash
Alex@MYLAPTOP:ls -c -d
wrong arguments
```

#### работа с глобальными переменными
```bash
Alex@MYLAPTOP:$HOME
Value of 'HOME' environment variable : None
```

#### Выход из консоли
```bash
Alex@MYLAPTOP:exit
Process finished with exit code 0
```

## Этап 2 Конфигурация

### Реализованный функционал

1. **Конфигурационный файл формата TOMl**: содержит в себе путь к VFS и путь к стартовому скрипту
2. **Логика приоритетов**:значения из командной строки имеют приоритет над
значениями из файла.
3. **Скрипты реальной ОС**: для выполнения эмулятора

Были созданы 3 скрипта которые отрабатывают следующим образом:

### test_config1
```bash
    Test 1: Run with config file
=== Starting File System Emulator ===
Loading configuration from: config.toml
Loaded vfs_path from config: ./vfs_storage
Loaded startup_script from config: ./startup.txt
=== Emulator Configuration ===
VFS Path: ./vfs_storage
Startup Script: ./startup.txt
Config File: config.toml
==============================
VFS directory already exists: ./vfs_storage
=== Executing startup script: ./startup.txt ===
Alex@MYLAPTOP: ls
LS command executed
Listing current directory
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: cd /home
CD command executed
Changing directory to: /home
Alex@MYLAPTOP: ls -l
LS command executed
Listing current directory
Arguments: ['-l']
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: cd /var
CD command executed
Changing directory to: /var
Alex@MYLAPTOP: ls -s
LS command executed
Listing current directory
Arguments: ['-s']
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: exit
Exiting emulator...
System shutdown completed
=== Startup script completed successfully ===

=== Starting interactive mode ===
Available commands: cd, ls, exit
Example: ls -l /home
Press Ctrl+C to exit

Alex@MYLAPTOP:
```

### test_noexist

```bash
noexist configuration file
=== Starting File System Emulator ===
Warning: Config file 'nonexistent.toml' not found, using command line arguments only
=== Emulator Configuration ===
VFS Path: Not set
Startup Script: Not set
Config File: nonexistent.toml
==============================

=== Starting interactive mode ===
Available commands: cd, ls, exit
Example: ls -l /home
Press Ctrl+C to exit

Alex@MYLAPTOP:
```

### test_all
```bash
Running all configuration tests...

=== Test 1: Config file ===
=== Starting File System Emulator ===
Loading configuration from: config.toml
Loaded vfs_path from config: ./vfs_storage
Loaded startup_script from config: ./startup.txt
=== Emulator Configuration ===
VFS Path: ./vfs_storage
Startup Script: ./startup.txt
Config File: config.toml
==============================
VFS directory already exists: ./vfs_storage
=== Executing startup script: ./startup.txt ===
Alex@MYLAPTOP: ls
LS command executed
Listing current directory
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: cd /home
CD command executed
Changing directory to: /home
Alex@MYLAPTOP: ls -l
LS command executed
Listing current directory
Arguments: ['-l']
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: cd /var
CD command executed
Changing directory to: /var
Alex@MYLAPTOP: ls -s
LS command executed
Listing current directory
Arguments: ['-s']
file1.txt  file2.txt  directory1/
Alex@MYLAPTOP: exit
Exiting emulator...
System shutdown completed
=== Startup script completed successfully ===

=== Starting interactive mode ===
Available commands: cd, ls, exit
Example: ls -l /home
Press Ctrl+C to exit

Alex@MYLAPTOP:
```