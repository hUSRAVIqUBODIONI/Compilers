# main.py
from lexer import Lexer
from parser import Parser
from ast import print_ast

def main():
   
    filename = "test.txt"
    with open(filename) as input_text:
      lexer = Lexer(input_text.read())
      tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    print_ast(ast)
    print("\n")
    for i in parser.errors:
        print(i,"\n")


if __name__ == "__main__":
    main()