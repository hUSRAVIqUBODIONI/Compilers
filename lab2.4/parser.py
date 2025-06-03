from typing import List, Optional
from lexer import Token, TokenType
from ast import Specification,ClassSection,TokensSection,TypesSection,TypeDef,MethodsSection,MethodDecl,MethodParam,Repetition,Symbol,GrammarRule,GrammarSection,Alternative,Item,Group,AxiomSection,EndSection

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token: Optional[Token] = None
        self.token_index = -1
        self.errors = []
        self.advance()
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
    
    def consume(self, token_type: TokenType, error_msg: str):
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            raise SyntaxError(f"{error_msg} at line {self.current_token.line}, column {self.current_token.column}")
            
    
    def parse(self) -> Specification:
        class_section = self.parse_class_section()
        tokens_section = self.parse_tokens_section()
        types_section = self.parse_types_section()
        methods_section = self.parse_methods_section()
        grammar_section = self.parse_grammar_section()
        axiom_section = self.parse_axiom_section()
        end_section = self.parse_end_section()
        return Specification(
            class_section=class_section,
            tokens_section=tokens_section,
            types_section = types_section,
            methods_section = methods_section,
            grammar_section = grammar_section,
            axiom_section = axiom_section,
            end_section = end_section
        )
    
    def parse_class_section(self) -> ClassSection:
        self.consume(TokenType.CLASS, "Expected '%class'")
        class_name = self.consume(TokenType.IDENTIFIER, "Expected class name").value
    
        return ClassSection(class_name=class_name)
    
    def parse_tokens_section(self) -> TokensSection:
        self.consume(TokenType.TOKENS, "Expected '%tokens'")
        tokens = []
        while self.current_token and self.current_token.type != TokenType.TYPES:
            self.consume(TokenType.IDENTIFIER,"Expected token declaration")
            tokens.append(self.current_token.value)
            self.advance()
       
        return TokensSection(tokens=tokens)
    
    def parse_types_section(self) -> TypesSection:
        self.consume(TokenType.TYPES, "Expected '%types'")
        type_defs = []
        while True:
            type_def = self.parse_type_def()
            type_defs.append(type_def)
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            else:
                break
       
        return TypesSection(type_defs=type_defs)
    
    def parse_type_def(self) -> TypeDef:
        types = []
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            type = self.current_token.value
            self.advance()
            if self.current_token and self.current_token.type == TokenType.COMMA:
               
                self.advance()
                
                 
            if self.current_token and self.current_token.type == TokenType.COLON:
                self.advance()
                 
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                    type += " : " +  self.current_token.value
                    self.advance()  
                    if self.current_token and self.current_token.type == TokenType.COMMA:     
                        self.advance()
                         
            types.append(type)
        return TypeDef(types=types)
    
    
    def parse_methods_section(self) -> MethodsSection:
        self.consume(TokenType.METHODS, "Expected '%methods'")
        method_decls = []
        while True:
            if self.current_token and (self.current_token.type == TokenType.SEMICOLON or self.current_token.type == TokenType.GRAMMAR ):
                break
            method_decl = self.parse_method_decl()
            method_decls.append(method_decl)
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
        return MethodsSection(method_decls=method_decls)
    
    def parse_method_decl(self) -> MethodDecl:
        
        return_type = self.consume(TokenType.IDENTIFIER, "Expected return type").value
        
        method_name = self.consume(TokenType.IDENTIFIER, "Expected method name").value
        
        self.consume(TokenType.LPAREN, "Expected '(' in method declaration")
        params = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            params = self.parse_params()
        self.consume(TokenType.RPAREN, "Expected ')' in method declaration")
        self.consume(TokenType.SEMICOLON, "Expected ';' after method declaration")
        return MethodDecl(
            return_type=return_type,
            method_name=method_name,
            params=params
        )
   
    def parse_params(self) -> List[MethodParam]:
        params = []
        while True:
            param_type = self.consume(TokenType.IDENTIFIER, "Expected parameter type").value
            if self.current_token and self.current_token.type == TokenType.LBRACKET:
                self.advance()
                self.consume(TokenType.RBRACKET,"Expected ] after [")
                param_type +="[]"
            params.append(MethodParam(param_type=param_type))
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break
        return params
    
    def parse_grammar_section(self) -> GrammarSection:
        self.consume(TokenType.GRAMMAR, "Expected '%grammar'")
        rules = []
        while True:
            if self.current_token and self.current_token.type in (TokenType.AXIOM, TokenType.EOF):
                print(self.current_token.value,"\n")
                break
           
            rule = self.parse_grammar_rule()
            rules.append(rule)
        return GrammarSection(rules=rules)
    
    def parse_grammar_rule(self) -> GrammarRule:
        non_terminal = self.consume(TokenType.IDENTIFIER, "Expected non-terminal").value
        self.consume(TokenType.EQUALS, "Expected '=' in grammar rule")
        alternatives = self.parse_alternatives()
        method_name = None
        if self.current_token and self.current_token.type == TokenType.SLASH:
            self.advance()
            method_name = self.consume(TokenType.IDENTIFIER, "Expected method name after '/'").value
        self.consume(TokenType.SEMICOLON,"Expected ; after end of rule")
        return GrammarRule(
            non_terminal=non_terminal,
            alternatives=alternatives,
            method_name=method_name
        )
    
    def parse_alternatives(self) -> List[Alternative]:
        alternatives = []
        while True:
            sequence = self.parse_sequence()
            method_name = None
            if self.current_token and self.current_token.type == TokenType.SLASH:
                self.advance()
                method_name = self.consume(TokenType.IDENTIFIER, "Expected method name after '/'").value
            alternatives.append(Alternative(sequence=sequence, method_name=method_name))
            if self.current_token and self.current_token.type == TokenType.OR:
                self.advance()
            else:
                break
        return alternatives
    
    def parse_sequence(self) -> List[Item]:
        items = []
        while True:
            if (not self.current_token or 
                self.current_token.type in (TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON,TokenType.RPAREN)):
                break
            item = self.parse_item()
            items.append(item)
        return items
    
    def parse_item(self) -> Item:
       
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            alternatives = self.parse_alternatives()
            self.consume(TokenType.RPAREN, "Expected ')' after group")
            return Group(alternatives=alternatives)
        elif self.current_token.type == TokenType.REP:
            
            self.advance()
            
            self.consume(TokenType.LPAREN, "Expected '(' after %rep")
            item = self.parse_alternatives()
            
            self.consume(TokenType.RPAREN, "Expected ')' after %rep item")
            return Repetition(item=item, is_rep=True)
        elif self.current_token.type == TokenType.IDENTIFIER:
            symbol = Symbol(name=self.current_token.value)
            self.advance()
            
                
            return symbol
        else:
            return
    
    def parse_axiom_section(self) -> AxiomSection:
    
        self.consume(TokenType.AXIOM, "Expected '%axiom'")
        axiom = self.consume(TokenType.IDENTIFIER, "Expected axiom name").value
        return AxiomSection(axiom=axiom)
    
    def parse_end_section(self) -> EndSection:
        self.consume(TokenType.END, "Expected '%end'")
        return EndSection()
