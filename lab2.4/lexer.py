import re
from enum import Enum

class TokenType(Enum):
    # Секции
    CLASS = "%class"
    TOKENS = "%tokens"
    TYPES = "%types"
    METHODS = "%methods"
    GRAMMAR = "%grammar"
    AXIOM = "%axiom"
    END = "%end"
    
    # Ключевые слова
    REP = "%rep"
    OR = "|"
    SLASH = "/"
    SEMICOLON = ";"
    COLON = ":"
    COMMA = ","
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    EQUALS = "="
    
    # Идентификаторы
    IDENTIFIER = "IDENTIFIER"
    
    # Конец файла
    EOF = "EOF"
    
    # Ошибка
    ERROR = "ERROR"

class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}, {self.column})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.keywords = {
            "%class": TokenType.CLASS,
            "%tokens": TokenType.TOKENS,
            "%types": TokenType.TYPES,
            "%methods": TokenType.METHODS,
            "%grammar": TokenType.GRAMMAR,
            "%axiom": TokenType.AXIOM,
            "%end": TokenType.END,
            "%rep": TokenType.REP,
            "|": TokenType.OR,
            "/": TokenType.SLASH,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON,
            ",": TokenType.COMMA,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            "[": TokenType.LBRACKET,
            "]": TokenType.RBRACKET,
            "=": TokenType.EQUALS,
        }
    
    def tokenize(self):
        while self.position < len(self.source):
            current_char = self.source[self.position]
            
            # Пропускаем пробельные символы
            if current_char.isspace():
                self._advance()
                continue
            
            # Обработка комментариев (начинаются с $)
            if current_char == '$':
                self._skip_comment()
                continue
            
            # Проверяем ключевые слова и символы
            matched = False
            for keyword, token_type in self.keywords.items():
                if self.source.startswith(keyword, self.position):
                    self.tokens.append(Token(token_type, keyword, self.line, self.column))
                    self.position += len(keyword)
                    self.column += len(keyword)
                    matched = True
                    break
            
            if matched:
                continue
            
            # Идентификаторы (начинаются с буквы, содержат буквы, цифры и дефисы)
            if re.match(r'[a-zA-Z]', current_char):
                start_pos = self.position
                while self.position < len(self.source) and re.match(r'[a-zA-Z0-9_\-]', self.source[self.position]):
                    self._advance()
                
                identifier = self.source[start_pos:self.position]
                self.tokens.append(Token(TokenType.IDENTIFIER, identifier, self.line, self.column - len(identifier)))
                continue
            
            # Неизвестный символ
            self.tokens.append(Token(TokenType.ERROR, current_char, self.line, self.column))
            self._advance()
        
        # Добавляем токен конца файла
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens
    
    def _advance(self):
        if self.position < len(self.source):
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _skip_comment(self):
        while self.position < len(self.source) and self.source[self.position] != '\n':
            self._advance()
        # Пропускаем символ новой строки
        if self.position < len(self.source) and self.source[self.position] == '\n':
            self._advance()
