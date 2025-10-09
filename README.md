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
## Этап 3. VFS

### Реализованный функционал

1. **VFS файл**: Формата CSV
2. **Обработка ошибок**
3. **Команда для сохранения VFS**: vfs-save
4. **Обработка ошибок**: Сообщения об неизвестных командах и неверных аргументах
5. **Базовые команды**: Реализованы команды `ls`, `cd` (заглушки) и `exit`

### Примеры

#### VFS
```angular2html
/
/usr
/usr/local
/usr/local/bin
/usr/local/bin/custom_app
/usr/share
/usr/share/docs
/usr/share/docs/manual
/usr/share/docs/manual/chapter1
/usr/share/docs/manual/chapter1/section1.txt
/usr/share/docs/manual/chapter1/section2.txt
/home
/home/alex
/home/alex/projects
/home/alex/projects/project1
/home/alex/projects/project1/src
/home/alex/projects/project1/src/main.py
/home/alex/projects/project1/src/utils.py
/home/alex/projects/project1/README.md
/tmp
```

#### Скрипт
```bash
Running all configuration tests...

=== Test 1: Config file ===
=== Starting File System Emulator ===
Loading configuration from: config.toml
Loaded vfs_path from config: ./vfs_storage
Loaded vfs_csv from config: vfs_medium.csv
Loaded startup_script from config: ./startup.txt
=== Emulator Configuration ===
VFS Path: ./vfs_storage
VFS CSV: vfs_medium.csv
Startup Script: ./startup.txt
Config File: config.toml
==============================
VFS directory already exists: ./vfs_storage
Loading VFS from: vfs_medium.csv
Added: /bin
Parent:
Child: bin
Added: /bin/ls
Parent: bin
Child: ls
Added: /bin/cd
Parent: bin
Child: cd
Added: /home
Parent:
Child: home
Added: /home/user1
Parent: home
Child: user1
Added: /home/user1/documents
Parent: user1
Child: documents
Added: /home/user1/documents/doc1.pdf
Parent: documents
Child: doc1.pdf
Added: /home/user1/documents/doc2.docx
Parent: documents
Child: doc2.docx
Added: /home/user1/.bashrc
Parent: user1
Child: .bashrc
Added: /var
Parent:
Child: var
Added: /var/log
Parent: var
Child: log
Added: /var/log/system.log
Parent: log
Child: system.log
VFS loaded successfully from vfs_medium.csv
=== Executing startup script: ./startup.txt ===
Alex@MYLAPTOP:/$ ls
Contents of /:
  bin/
  home/
  var/
Alex@MYLAPTOP:/$ cd /home
Alex@MYLAPTOP:/home$ ls
Contents of /home:
  user1/
Alex@MYLAPTOP:/home$ cd alex
ERROR: path home/alex not exist
Error: Directory 'alex' not found
Failed to change directory to: alex
Alex@MYLAPTOP:/home$ ls
Contents of /home:
  user1/
Alex@MYLAPTOP:/home$ cd projects/project1
ERROR: path home/projects/project1 not exist
Error: Directory 'projects/project1' not found
Failed to change directory to: projects/project1
Alex@MYLAPTOP:/home$ ls
Contents of /home:
  user1/
Alex@MYLAPTOP:/home$ cd /nonexistent
ERROR: path nonexistent not exist
Error: Directory '/nonexistent' not found
Failed to change directory to: /nonexistent
Alex@MYLAPTOP:/home$ ls /invalid/path
ERROR: path invalid/path not exist
Error: Path '/invalid/path' not found
Alex@MYLAPTOP:/home$ vfs-save /tmp/backup.csv
VFS would be saved to: /tmp/backup.csv
VFS saved successfully to: /tmp/backup.csv
Alex@MYLAPTOP:/home$ $HOME
Value of 'HOME' environment variable: None
Alex@MYLAPTOP:/home$ $USER
Value of 'USER' environment variable: None
Alex@MYLAPTOP:/home$ exit
Exiting emulator...
System shutdown completed
=== Startup script completed successfully ===

=== Starting interactive mode ===
Available commands: cd, ls, exit
Example: ls -l /home
Press Ctrl+C to exit

Alex@MYLAPTOP:/home$ cd user1
Alex@MYLAPTOP:/home/user1$
```