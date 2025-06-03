from typing import List, Optional, Set, cast
from lexer import Token, TokenType
from ast import Specification, ClassSection, TokensSection, TypesSection, TypeDef, MethodsSection, MethodDecl, MethodParam, Repetition, Symbol, GrammarRule, GrammarSection, Alternative, Item, Group, AxiomSection, EndSection

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current_token: Optional[Token] = None
        self.token_index = -1
        self.errors: List[str] = []   
        self.advance()
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
    
    def add_error(self, message: str):
        if self.current_token:
            error_msg = f"{message} at line {self.current_token.line}, column {self.current_token.column}"
        else:
            error_msg = f"{message} at end of input"
        self.errors.append(error_msg)
        return None
    
    def consume(self, token_type: TokenType, error_msg: str) -> Optional[Token]:
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        
        self.add_error(error_msg)
        
         
        if self.current_token:
            self.advance()
        return None
    
    def synchronize(self, sync_tokens: Set[TokenType]):
        while self.current_token:
            if self.current_token.type in sync_tokens:
                return
            self.advance()
    
    def synchronize_to_next_section(self):
        section_starts = {
            TokenType.CLASS, TokenType.TOKENS, TokenType.TYPES,
            TokenType.METHODS, TokenType.GRAMMAR, TokenType.AXIOM, TokenType.END
        }
        while self.current_token and self.current_token.type not in section_starts:
            self.advance()
    
    def parse(self) -> Specification:
        sections = []
        section_parsers = [
            self.parse_class_section,
            self.parse_tokens_section,
            self.parse_types_section,
            self.parse_methods_section,
            self.parse_grammar_section,
            self.parse_axiom_section,
            self.parse_end_section
        ]
        
        for parser in section_parsers:
            try:
                section = parser()
                if section:   
                    sections.append(section)
            except Exception as e:
                self.add_error(f"Critical error in section: {str(e)}")
                self.synchronize_to_next_section()
        
         
        return Specification(
            class_section=sections[0] if len(sections) > 0 else ClassSection(""),
            tokens_section=sections[1] if len(sections) > 1 else TokensSection([]),
            types_section=sections[2] if len(sections) > 2 else TypesSection([]),
            methods_section=sections[3] if len(sections) > 3 else MethodsSection([]),
            grammar_section=sections[4] if len(sections) > 4 else GrammarSection([]),
            axiom_section=sections[5] if len(sections) > 5 else AxiomSection(""),
            end_section=sections[6] if len(sections) > 6 else EndSection()
        )
    
    def parse_class_section(self) -> ClassSection:
        self.consume(TokenType.CLASS, "Expected '%class'")
        class_name_token = self.consume(TokenType.IDENTIFIER, "Expected class name")
        class_name = class_name_token.value if class_name_token else "<missing>"
        return ClassSection(class_name=class_name)
    
    def parse_tokens_section(self) -> TokensSection:
        self.consume(TokenType.TOKENS, "Expected '%tokens'")
        tokens = []
        
         
        section_starts = {
            TokenType.CLASS, TokenType.TYPES, TokenType.METHODS,
            TokenType.GRAMMAR, TokenType.AXIOM, TokenType.END
        }
        
        while self.current_token and self.current_token.type not in section_starts:
            if self.current_token.type == TokenType.IDENTIFIER:
                tokens.append(self.current_token.value)
                self.advance()
            else:
                self.add_error(f"Unexpected token in tokens section: {self.current_token.value}")
                self.advance()
        
        return TokensSection(tokens=tokens)
    
    def parse_types_section(self) -> TypesSection:
        self.consume(TokenType.TYPES, "Expected '%types'")
        type_defs = []
        
         
        section_starts = {
            TokenType.CLASS, TokenType.TOKENS, TokenType.METHODS,
            TokenType.GRAMMAR, TokenType.AXIOM, TokenType.END
        }
        
        while self.current_token and self.current_token.type not in section_starts:
            try:
                type_def = self.parse_type_def()
                if type_def:
                    type_defs.append(type_def)
            except Exception as e:
                self.add_error(f"Error in type definition: {str(e)}")
                 
                self.synchronize({TokenType.SEMICOLON} | section_starts)
            
             
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            elif self.current_token and self.current_token.type not in section_starts:
                self.add_error("Expected ';' after type definition")
                self.synchronize(section_starts)
        
        return TypesSection(type_defs=type_defs)
    
    def parse_type_def(self) -> TypeDef:
        types = []
        
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            type_name = self.current_token.value
            self.advance()
            
             
            if self.current_token and self.current_token.type == TokenType.COLON:
                self.advance()
                 
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                    type_name += ":" + self.current_token.value
                    self.advance()
                else:
                    self.add_error("Expected type identifier after ':'")
            
            types.append(type_name)
            
             
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break
        
        if not types:
            self.add_error("Expected at least one type in type definition")
            return None
        
        return TypeDef(types=types)
    
    def parse_methods_section(self) -> MethodsSection:
        self.consume(TokenType.METHODS, "Expected '%methods'")
        method_decls = []
        
         
        section_starts = {
            TokenType.CLASS, TokenType.TOKENS, TokenType.TYPES,
            TokenType.GRAMMAR, TokenType.AXIOM, TokenType.END
        }
        
        while self.current_token and self.current_token.type not in section_starts:
            try:
                method_decl = self.parse_method_decl()
                if method_decl:
                    method_decls.append(method_decl)
            except Exception as e:
                self.add_error(f"Error in method declaration: {str(e)}")
                 
                self.synchronize({TokenType.SEMICOLON} | section_starts)
            
             
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
        
        return MethodsSection(method_decls=method_decls)
    
    def parse_method_decl(self) -> MethodDecl:
        return_type_token = self.consume(TokenType.IDENTIFIER, "Expected return type")
        return_type = return_type_token.value if return_type_token else "<missing>"
        
        method_name_token = self.consume(TokenType.IDENTIFIER, "Expected method name")
        method_name = method_name_token.value if method_name_token else "<missing>"
        
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
        
        while self.current_token and self.current_token.type != TokenType.RPAREN:
            param_type_token = self.consume(TokenType.IDENTIFIER, "Expected parameter type")
            if not param_type_token:
                 
                self.synchronize({TokenType.COMMA, TokenType.RPAREN})
                continue
            
            param_type = param_type_token.value
            
             
            if self.current_token and self.current_token.type == TokenType.LBRACKET:
                self.advance()
                self.consume(TokenType.RBRACKET, "Expected ']' after '['")
                param_type += "[]"
            
            params.append(MethodParam(param_type=param_type))
            
             
            if self.current_token and self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break
        
        return params
    
    def parse_grammar_section(self) -> GrammarSection:
        self.consume(TokenType.GRAMMAR, "Expected '%grammar'")
        rules = []
        
         
        section_starts = {
            TokenType.CLASS, TokenType.TOKENS, TokenType.TYPES,
            TokenType.METHODS, TokenType.AXIOM, TokenType.END
        }
        
        while self.current_token and self.current_token.type not in section_starts:
            try:
                rule = self.parse_grammar_rule()
                if rule:
                    rules.append(rule)
            except Exception as e:
                self.add_error(f"Error in grammar rule: {str(e)}")
                 
                self.synchronize({TokenType.SEMICOLON} | section_starts)
                if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                    self.advance()
        
        return GrammarSection(rules=rules)
    
    def parse_grammar_rule(self) -> GrammarRule:
        non_terminal_token = self.consume(TokenType.IDENTIFIER, "Expected non-terminal")
        non_terminal = non_terminal_token.value if non_terminal_token else "<missing>"
        
        self.consume(TokenType.EQUALS, "Expected '=' in grammar rule")
        
         
        rule_end = {TokenType.SEMICOLON, TokenType.AXIOM, TokenType.END}
        
        alternatives = []
        try:
            alternatives = self.parse_alternatives()
        except Exception:
            self.add_error("Error parsing alternatives")
            self.synchronize(rule_end)
        
        method_name = None
        if self.current_token and self.current_token.type == TokenType.SLASH:
            self.advance()
            method_name_token = self.consume(TokenType.IDENTIFIER, "Expected method name after '/'")
            if method_name_token:
                method_name = method_name_token.value
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after end of rule")
        
        return GrammarRule(
            non_terminal=non_terminal,
            alternatives=alternatives,
            method_name=method_name
        )
    
    def parse_alternatives(self) -> List[Alternative]:
        alternatives = []
        
        while True:
            sequence = []
            try:
                sequence = self.parse_sequence()
            except Exception:
                self.add_error("Error parsing sequence")
                 
                self.synchronize({TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON})
            
            method_name = None
            if self.current_token and self.current_token.type == TokenType.SLASH:
                self.advance()
                method_name_token = self.consume(TokenType.IDENTIFIER, "Expected method name after '/'")
                if method_name_token:
                    method_name = method_name_token.value
            
            alternatives.append(Alternative(sequence=sequence, method_name=method_name))
            
            if self.current_token and self.current_token.type == TokenType.OR:
                self.advance()
            else:
                break
        
        return alternatives
    
    def parse_sequence(self) -> List[Item]:
        items = []
        
        while self.current_token and self.current_token.type not in {
            TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON, TokenType.RPAREN
        }:
            try:
                item = self.parse_item()
                if item:
                    items.append(item)
            except Exception:
                self.add_error("Error parsing grammar item")
                 
                self.synchronize({
                    TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON, 
                    TokenType.RPAREN, TokenType.IDENTIFIER,
                    TokenType.LPAREN, TokenType.REP
                })
        
        return items
    
    def parse_item(self) -> Optional[Item]:
        if not self.current_token:
            return None
            
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
            self.add_error(f"Unexpected item in grammar: {self.current_token.value}")
            self.advance()
            return None
    
    def parse_axiom_section(self) -> AxiomSection:
        self.consume(TokenType.AXIOM, "Expected '%axiom'")
        axiom_token = self.consume(TokenType.IDENTIFIER, "Expected axiom name")
        axiom = axiom_token.value if axiom_token else "<missing>"
        return AxiomSection(axiom=axiom)
    
    def parse_end_section(self) -> EndSection:
        self.consume(TokenType.END, "Expected '%end'")
        return EndSection()