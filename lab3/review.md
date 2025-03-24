% Лабораторная работа № 1.3 «Объектно-ориентированный
  лексический анализатор»
% 11 марта 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является приобретение навыка реализации лексического анализатора на 
объектно-ориентированном языке без применения каких-либо средств автоматизации решения 
задачи лексического анализа.

# Индивидуальный вариант
Числа: последовательности десятичных цифр, могут начинаться с нуля.
Знаки операций: «+», «-», «*», «/», «(», «)».
Комментарии начинаются на «(*», заканчиваются на «*)», не могут быть вложенными.
Строки: ограничены фигурными скобками «{ … }», escape-последовательности «#{», «#}», «##», 
«#hh», означают, соответственно «{», «}», «#» и символ с кодом hh, где h — шестнадцатеричное 
число, не могут пересекать границы строчек ткста.

# Реализация

Файл `Position.py`
```python
class Position:
    def __init__(self, line=1, pos=1):
        self.line = line  # Номер текущей строки
        self.pos = pos    # Позиция в текущей строке

    def Line(self):
        return self.line

    def Pos(self):
        return self.pos

    def __lt__(self, other):  # <
        return (self.line, self.pos) < (other.line, other.pos)

    def __eq__(self, other):  # ==
        return (self.line, self.pos) == (other.line, other.pos)

    def __le__(self, other):  # <=
        return (self.line, self.pos) <= (other.line, other.pos)

    def ToString(self):
        return f"({self.line}, {self.pos})"

    def next(self, char):
        if char == '\n':
            self.line += 1
            self.pos = 1
        else:
            self.pos += 1
        return self
class Fragment:
    def __init__(self, starting, following):
        self.Starting = starting
        self.Following = following

    def ToString(self):
        return f"{self.Starting.ToString()} - {self.Following.ToString()}"

class Message:
    def __init__(self, IsError, Pos ,Text):
        self.IsError = IsError
        self.Position = Pos
        self.Text = Text
```

Файл `Token.py`
```python
class DomainTag(enum.Enum):
    NUMBER = 1,
    CHAR = 2,
    LPAREN = 3,  # (
    RPAREN = 4,  # )
    PLUS = 5,
    MINUS = 6,
    MULTIPLY = 7,
    DIVIDE = 8,
    STRING = 9  # Строка
    COMMENT = 10  # Комментарий
    END_OF_PROGRAM = 11

class Token:
    def __init__(self, tag, starting, following):
        self.Tag = tag
        self.Coords = Fragment(starting, following)

class NumberToken(Token):
    def __init__(self, starting, following, value: int):
        super().__init__(DomainTag.NUMBER, starting, following)
        self.value = value  # Атрибут: значение числа

    def __str__(self):
        return f"NUMBER {self.Coords.ToString()}: {self.value}"

class CharToken(Token):
    def __init__(self, starting, following, char: str):
        super().__init__(DomainTag.CHAR, starting, following)
        self.char = char  # Атрибут: символ

    def __str__(self):
        return f"CHAR {self.Coords.ToString()}: {self.char}"

class StringToken(Token):
    def __init__(self, starting, following, value: str):
        super().__init__(DomainTag.STRING, starting, following)
        self.value = value  # Атрибут: значение строки

    def __str__(self):
        return f"STRING {self.Coords.ToString()}: {self.value}"

class SpecToken(Token):
    def __init__(self, tag: DomainTag, starting: Position, following: Position):
        assert tag in {
            DomainTag.LPAREN,
            DomainTag.RPAREN,
            DomainTag.PLUS,
            DomainTag.MINUS,
            DomainTag.MULTIPLY,
            DomainTag.DIVIDE,
            DomainTag.END_OF_PROGRAM
        }, f"Invalid tag for SpecToken: {tag}"
        super().__init__(tag, starting, following)

    def __str__(self):
        return f"SPEC {self.Coords.ToString()}: {self.Tag.name}"
```

Файл `Lexer.py`
```python
class Lexer:
    def __init__(self):
        self.position = Position()  # Текущая позиция в тексте
        self.tokens: List[Token] = []  # Список распознанных токенов
        self.comments: List[Fragment] = []  # Список комментариев
        self.errors: List[Message] = []  # Список ошибок

    def NextToken(self, char):
        if char.isspace():
            self.position.next(char)
            return None

        start = Position(self.position.line, self.position.pos)

        if char == '(':
            next_char = sys.stdin.read(1)
            if  next_char != '*':
                self.position.next(char)
                end = Position(self.position.line, self.position.pos)
                self.tokens.append(SpecToken(DomainTag.LPAREN, start, end))
                print(SpecToken(DomainTag.LPAREN, start, end))
                return self.NextToken(next_char)
            else:
                self.position.next(char)
                self.position.next(next_char)
                comment_start = start
                while True:
                    char = sys.stdin.read(1)
                    if not char:
                        self.errors.append(Message(True, self.position, "unclosed comment"))
                        break
                    if char == '*' and sys.stdin.read(1) == ')':
                        self.position.next(char)
                        self.position.next(')')
                        break
                    self.position.next(char)
                end = Position(self.position.line, self.position.pos)
                self.comments.append(Fragment(comment_start, end))
                return None

        elif char == ')':
            self.position.next(char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(SpecToken(DomainTag.RPAREN, start, end))
            return SpecToken(DomainTag.RPAREN, start, end)

        elif char == '*':
            self.position.next(char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(SpecToken(DomainTag.MULTIPLY, start, end))
            return SpecToken(DomainTag.MULTIPLY, start, end)

        elif char == '-':
            self.position.next(char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(SpecToken(DomainTag.MINUS, start, end))
            return SpecToken(DomainTag.MINUS, start, end)

        elif char == '+':
            self.position.next(char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(SpecToken(DomainTag.PLUS, start, end))
            return SpecToken(DomainTag.PLUS, start, end)

        elif char == '/':
            self.position.next(char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(SpecToken(DomainTag.DIVIDE, start, end))
            return SpecToken(DomainTag.DIVIDE, start, end)

        elif char == '{':
            name = ""
            self.position.next(char)
            while True:
                char = sys.stdin.read(1)
                if not char or char == '}':
                    break
                if char == '#':
                    escape_char = sys.stdin.read(1)
                    if escape_char == '#':
                        name += '#'
                        self.position.next('#')
                    elif escape_char == '{':
                        name += '{'
                        self.position.next('{')
                    elif escape_char == '}':
                        name += '}'
                        self.position.next('}')
                    elif escape_char.isalnum():
                        hex_code = escape_char
                        next_char = sys.stdin.read(1)
                        if next_char.isalnum():
                            hex_code += next_char
                            try:
                                char_code = str(int(hex_code, 16))
                                name += char_code
                                self.position.next(escape_char)
                                self.position.next(next_char)
                            except ValueError:
                                self.errors.append(Message(True, self.position, 
"invalid hex escape sequence"))
                        else:
                            self.errors.append(Message(True, self.position, 
"incomplete hex escape sequence"))
                    else:
                        self.errors.append(Message(True, self.position, 
"unrecognized escape sequence"))
                else:
                    name += char
                    self.position.next(char)
            if char == '}':
                self.position.next(char)
                end = Position(self.position.line, self.position.pos)
                self.tokens.append(StringToken(start, end, name))
                return StringToken(start, end, name)
            else:
                self.errors.append(Message(True, start, "unclosed string literal"))
                return None

        elif char == '\'':
            char = sys.stdin.read(1)
            if char == '\n':
                self.errors.append(Message(True, start, "newline in constant"))
                self.position.next('\n')
                return None
            elif char == '\\':
                escape_char = sys.stdin.read(1)
                if escape_char == 'n':
                    char = '\n'
                elif escape_char == '\'':
                    char = '\''
                elif escape_char == '\\':
                    char = '\\'
                else:
                    self.errors.append(Message(True, self.position, 
"unrecognized escape sequence"))
                    return None
            next_char = sys.stdin.read(1)
            if next_char != '\'':
                self.errors.append(Message(True, self.position, 
"too many characters in character literal"))
                return None
            self.position.next(char)
            self.position.next(next_char)
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(CharToken(start, end, char))
            return CharToken(start, end, char)

        elif char.isdigit():
            val = int(char)
            self.position.next(char)
           
            try:
                while True:
                    char = sys.stdin.read(1)
                    if not char or not char.isdigit():
                        break
                    self.position.next(char)
                    val = val * 10 + int(char)
                if val > 2**63 - 1:  
                    raise OverflowError("integral constant is too large")               
            except OverflowError:
                self.errors.append(Message(True, start, "integral constant is too large"))
                
            end = Position(self.position.line, self.position.pos)
            self.tokens.append(NumberToken(start, end, val))
            return NumberToken(start, end, val)

        else:
            self.errors.append(Message(True, start, f"unexpected character: {char}"))
            self.position.next(char)
            return None

    def Finalize(self):
        end = Position(self.position.line, self.position.pos)
        self.tokens.append(SpecToken(DomainTag.END_OF_PROGRAM, end, end))
        return self.tokens

```

# Тестирование

Входные данные

```
(* hello world *)
{HEllo ## #AA #{  #AA ## HELO  #}}
999999999999999999999999999999999999999999999999999999999999
a 1
```

Вывод на `stdout`

```
Tokens:
STRING (2, 1) - (2, 35): HEllo # 170 {  170 # HELO  }
NUMBER (3, 1) - (3, 61): 9999999999999999999
NUMBER (4, 3) - (4, 4): 1
SPEC (6, 1) - (6, 1): END_OF_PROGRAM


Errors:
integral constant is too large (3, 1)
unexpected symbol (4, 1)


Comments:
(1, 1) - (1, 18)
```

# Вывод

Мне понравилось выполнять эту лабораторную работу, потому что она была интересной и 
познавательной. Особенно впечатлила реализация отслеживания координат токенов — это 
важная часть лексического анализа, которая помогает точно находить ошибки и понимать, 
где именно в тексте программы они возникли. Сам бы я до такого решения не додумался, 
поэтому было полезно разобраться, как это работает.

В процессе работы я научился разбирать исходный текст программы на токены, такие как числа, 
символы, строки и операторы. Я также разобрался, как обрабатывать специальные символы и 
escape-последовательности в строках и символьных литералах. Ещё я понял, как важно отслеживать 
позиции токенов в тексте, чтобы можно было точно указывать, где возникла ошибка. Кроме того, 
я научился пропускать комментарии и обрабатывать различные ошибки, например, незакрытые строки, 
неверные символы или слишком большие числа.

Эта работа помогла мне лучше понять, как устроены лексические анализаторы и какие сложности 
могут возникать при их создании. Теперь я знаю, как важно учитывать каждую мелочь при обработке 
текста, и это пригодится мне в дальнейшем изучении компиляторов и программирования в целом. 
В целом, лабораторная работа была полезной и интересной, и я доволен результатом.
