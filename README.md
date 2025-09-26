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