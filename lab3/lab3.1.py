import re
from typing import List, Union
import unicodedata
import enum

class Position:
    def __init__(self, text, line=1, pos=1, index=0):
        self.text = text  # Исходный текст программы
        self.line = line  # Номер текущей строки
        self.pos = pos    # Позиция в текущей строке
        self.index = index  # Индекс в тексте

    def Line(self):
        return self.line

    def Pos(self):
        return self.pos

    def Index(self):
        return self.index

    def __lt__(self, other):  # <
        return self.index < other.index

    def __eq__(self, other):  # ==
        return self.index == other.index

    def __le__(self, other):  # <=
        return self.index <= other.index

    def ToString(self):
        return f"({self.line}, {self.pos})"

    def Cp(self):
        return -1 if self.index == len(self.text) else self.text[self.index]

    def Uc(self):
        return "OtherNotAssigned" if self.index == len(self.text) else unicodedata.category(chr(self.Cp()))

    def isWhiteSpace(self):
        return self.index != len(self.text) and self.text[self.index].isspace()

    def IsLetter(self):
        return self.index != len(self.text) and self.text[self.index].isalpha()

    def IsLetterOrDigit(self):
        return self.index != len(self.text) and (self.text[self.index].isalpha() or ('0' <= self.text[self.index] <= '9'))

    def IsDecimalDigit(self):
        return self.index != len(self.text) and ('0' <= self.text[self.index] <= '9')

    def IsNewLine(self):
        if self.index == len(self.text):
            return True
        if self.text[self.index] == '\r' and self.index + 1 < len(self.text):
            return self.text[self.index + 1] == '\n'
        return self.text[self.index] == '\n'

    def next(self):
        if self.index < len(self.text):
            if self.IsNewLine():
                if self.text[self.index] == '\r':
                    self.index += 1
                self.line += 1
                self.pos = 1
            else:
                if 0xD800 <= ord(self.text[self.index]) <= 0xDBFF:
                    self.index += 1
                self.pos += 1
            self.index += 1
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
        # Проверяем, что tag является допустимым значением
        assert tag in {
            DomainTag.LPAREN,
            DomainTag.RPAREN,
            DomainTag.PLUS,
            DomainTag.MINUS,
            DomainTag.MULTIPLY,
            DomainTag.DIVIDE,
            DomainTag.END_OF_PROGRAM
        }, f"Invalid tag for SpecToken: {tag}"

        # Вызываем конструктор базового класса
        super().__init__(tag, starting, following)

    def __str__(self):
        return f"SPEC {self.Coords.ToString()}: {self.Tag.name}"


class Lexer:
    def __init__(self, program: str):
        self.program = program  # Исходный текст программы
        self.position = Position(program)  # Текущая позиция в тексте
        self.tokens: List[Token] = []  # Список распознанных токенов
        self.comments: List[Fragment] = []  # Список комментариев
        self.errors: List[Message] = []  # Список ошибок

    def NextToken(self):
        while self.position.Cp() != -1:
            
            while self.position.isWhiteSpace():
                
                self.position.next()
            start = Position(self.program,self.position.line,self.position.pos,self.position.index)

            match self.position.Cp():
                case '(':
                    
                    if self.position.next().Cp() != '*':
                        end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        self.tokens.append(SpecToken(DomainTag.LPAREN,start,end))
                        continue
                    
                    while self.position.Cp() != ')' and self.position.Cp() != -1:
                        while self.position.Cp() != '*' and self.position.Cp() != -1:
                            self.position.next()
                        self.position.next()
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    if self.position.Cp() == -1:
                        ErrorMsg = Message(True,end,"end of program found, *) expected")
                        self.errors.append(ErrorMsg)
                        break
                    
                    self.comments.append(Fragment(start,end))
                    
                  
                    

                case ')':
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.tokens.append(SpecToken(DomainTag.RPAREN,start,end))
                 
      
                case '*':
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.tokens.append(SpecToken(DomainTag.MULTIPLY,start,end))
               

                case '-':
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.tokens.append(SpecToken(DomainTag.MINUS,start,end))
                  

                case '+':
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.tokens.append(SpecToken(DomainTag.PLUS,start,end))
        

                case '/':
                    self.position.next()
                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.tokens.append(SpecToken(DomainTag.DIVIDE,start,end))
                case '{':
                    name = ""
                    start = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    self.position.next()
                  
                    while self.position.Cp() != '}' and self.position.Cp() != -1:
                        if self.position.Cp() == '#':
                            temp = Position(self.program,self.position.line,self.position.pos,self.position.index)
                            self.position.next()
                            if self.position.Cp() =='#':
                                name+="#"
                                self.position.next()
                           
                            elif self.position.Cp() =='{':
                                name+="{"
                                self.position.next()
                                
                            elif self.position.Cp() =='}':
                                name+="}"
                                self.position.next()
                                
                            elif not re.search(r"[^A-F0-9]", self.position.Cp()):
                                hex_code = self.position.Cp()  # Первая шестнадцатеричная цифра
                                self.position.next()
                                if not re.search(r"[^A-F0-9]", self.position.Cp()):  # Вторая шестнадцатеричная цифра
                                    hex_code += self.position.Cp()
                                    self.position.next()
                                    try:
                                        name += str(int(hex_code, 16))  # Преобразуем hex в символ
                                    except ValueError:
                                        self.errors.append(Message(True, temp, "invalid hex escape sequence"))
                                else:
                                    self.errors.append(Message(True, temp, "incomplete hex escape sequence"))
                            else:
                                self.errors.append(Message(True,temp, "unrecognized escape sequence"))
                                        
                        else:
                            name += self.position.Cp() 
                            self.position.next()

                    if self.position.Cp() == '}':  
                        self.position.next() 
                        end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        self.tokens.append(StringToken(start, end, name))
                    else:  
                        self.errors.append(Message(True, start, "unclosed string literal"))


                case '\'':
                    temp = Position(self.program,self.position.line,self.position.pos,self.position.index)
                    if temp.next().IsNewLine():
                       
                        ErrorMsg = Message(True, temp,"Newline in constant")
                        self.errors.append(ErrorMsg)
                        self.tokens.append(CharToken(start,temp,"0"))
                        self.position = temp.next()
                    elif self.position.Cp() == '\\':
                        end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        ErrorMsg = Message(True, end,"empty character literal")
                        self.errors.append(ErrorMsg)
                        self.tokens.append(CharToken(start,end,"0"))
                        self.position.next()
                    else:
                        
                        ch = temp.Cp()
                        if ch == '\\':
                            match self.position.next().Cp():
                                case 'n':
                                    ch = 'n'
                                case '\'':
                                    ch = '\''
                                case '\\':
                                    ch = '\\'
                                case _:
                                    end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                                    ErrorMsg = Message(True, end,"unrecognized Escape sequence")
                                    self.errors.append(ErrorMsg)
                        if self.position.next().Cp() != '\'':
                            end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                            ErrorMsg = Message(True, end,"too many characters in character literal")
                            self.errors.append(ErrorMsg)
                            while self.position.Cp() !='\'' and not(self.position.IsNewLine()):
                                self.position.next()
                            if self.position.Cp() !='\'':
                                end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                                ErrorMsg = Message(True, end,"newline in  constant")
                                self.errors.append(ErrorMsg)
                        
                        end = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        self.tokens.append(CharToken(start,end,ch))

                case _:
                    if self.position.IsDecimalDigit():
                        start = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        val = ord(self.position.Cp()) - ord('0') 
                        self.position.next()  
                        try:
                            while self.position.IsDecimalDigit():
                                val = val * 10 + (ord(self.position.Cp()) - ord('0'))
                                if val > 2**63 - 1:  
                                    raise OverflowError("integral constant is too large")
                                self.position.next()
                        except OverflowError:
                            self.errors.append(Message(True, start, "integral constant is too large"))
                            while self.position.IsDecimalDigit():  
                                self.position.next()
                        if self.position.IsLetter():  
                            self.errors.append(Message(True, start, "delimiter required"))
                            while self.position.IsLetterOrDigit():  
                                self.position.next()
                        end =  Position(self.program,self.position.line,self.position.pos,self.position.index)
                        self.tokens.append(NumberToken(start, end, val))
                    else:
                        start = Position(self.program,self.position.line,self.position.pos,self.position.index)
                        self.errors.append(Message(True, start, "unexpected symbol"))
                        
                        self.position.next()
                        

    
          
        self.tokens.append(SpecToken(DomainTag.END_OF_PROGRAM,self.position,self.position.next()))
        return self.tokens



if __name__ == "__main__":
    file = open('/Users/husravi_qubodioni/Desktop/Compiletor/lab3/test.txt','r')
    content = file.read()
    
    lexer = Lexer(content)
    token = lexer.NextToken()
    print("Tokens:")
    for i in token:
        print(str(i))
    print("\n")
    print("Errors:")
    for i in lexer.errors[:-1]:
        print(i.Text,i.Position.ToString())
    file.close()
