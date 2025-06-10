from typing import List, Optional, Set
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
    
    def consume(self, token_type: TokenType, error_msg: str,need_advance = True) -> Optional[Token]:
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        
        self.add_error(error_msg)
        
         
        if self.current_token and need_advance:
            self.advance()
        return None
    
    def synchronize(self, sync_tokens: Set[TokenType]):
        while self.current_token:
            if self.current_token.type in sync_tokens:
                return
            self.advance()
    
    
    
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
    
    #<ClassSection> ::= "%class" <ClassName> 
    def parse_class_section(self) -> ClassSection:
        self.consume(TokenType.CLASS, "Expected '%class'")
        class_name_token = self.consume(TokenType.IDENTIFIER, "Expected class name")
        class_name = class_name_token.value if class_name_token else "<missing>"
        return ClassSection(class_name=class_name)
    
    #<TokensSection> ::= "%tokens" <TokenList> "\n"
    def parse_tokens_section(self) -> TokensSection:
        self.consume(TokenType.TOKENS, "Expected '%tokens'")
        tokens = []
        
        #<TokenList> ::= IDENTIFIER*
        while self.current_token and self.current_token.type != TokenType.TYPES:
            if self.current_token.type == TokenType.IDENTIFIER:
                tokens.append(self.current_token.value)
                self.advance()
            else:
                self.add_error(f"Expected token in tokens section: {self.current_token.value}")
                self.advance()
        
        return TokensSection(tokens=tokens)
    

    #<TypesSection> ::= "%types" <TypeDefs> "\n"
    def parse_types_section(self) -> TypesSection:
        self.consume(TokenType.TYPES, "Expected '%types'")
        type_defs = []
        
         
        #<TypeDefs> ::= <TypeDef> (";" <TypeDef>)*
        while self.current_token and self.current_token.type !=  TokenType.METHODS:

            type_def = self.parse_type_def()
            if type_def:
                type_defs.append(type_def)
            if self.current_token and self.current_token.type == TokenType.SEMICOLON:
                self.advance()
            elif self.current_token:
                self.add_error("Expected ';' after type definition")
                self.synchronize({TokenType.IDENTIFIER,TokenType.METHODS})
        
        return TypesSection(type_defs=type_defs)
    
    #<TypeDef> ::= IDENTIFIER ("," IDENTIFIER)*
    def parse_type_def(self) -> TypeDef:
        types = []
        type = ""
        while self.current_token and self.current_token.type == TokenType.IDENTIFIER:
            type_name = self.current_token.value
            
            self.advance()
            
             
            if self.current_token and self.current_token.type == TokenType.COLON:
                self.advance()
                 
                if self.current_token and self.current_token.type == TokenType.IDENTIFIER:
                    type = self.current_token.value
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
        
        if  type =="":
            self.add_error("Expected type after type definition")
            return None
        
        return TypeDef(name=types,type = type)
    
   
    #<MethodsSection> ::= "%methods" <MethodDecls> "\n"
    def parse_methods_section(self) -> MethodsSection:
        self.consume(TokenType.METHODS, "Expected '%methods'")
        method_decls = []
        
        #<MethodDecls> ::= <MethodDecl> ("\n" <MethodDecl>)*
        while self.current_token and self.current_token.type != TokenType.GRAMMAR:
            method_decl = self.parse_method_decl()
            if method_decl:
                method_decls.append(method_decl)
        
        return MethodsSection(method_decls=method_decls)
    
    #<MethodDecl> ::= <ReturnType> IDENTIFIER "(" <Params> ")" ";"
    def parse_method_decl(self) -> MethodDecl:
        return_type_token = self.consume(TokenType.IDENTIFIER, "Expected return type")
        return_type = return_type_token.value if return_type_token else "<missing>"
        
        method_name_token = self.consume(TokenType.IDENTIFIER, "Expected method name",False)
        method_name = method_name_token.value if method_name_token else "<missing>"
        
        self.consume(TokenType.LPAREN, "Expected '(' in method declaration",False)
        
        params = []
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            params = self.parse_params()
        
        self.consume(TokenType.RPAREN, "Expected ')' in method declaration",False)
        self.consume(TokenType.SEMICOLON, "Expected ';' after method declaration",False)
        
        return MethodDecl(
            return_type=return_type,
            method_name=method_name,
            params=params
        )
    
    #<Params> ::= <Param> ("," <Param>)* | ε
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
    

    #<GrammarSection> ::= "%grammar" "\n" <GrammarRules>
    def parse_grammar_section(self) -> GrammarSection:
        self.consume(TokenType.GRAMMAR, "Expected '%grammar'")
        rules = []
        
        
        #<GrammarRules>   ::= <GrammarRule> (<GrammarRules>)*
        while self.current_token and self.current_token.type != TokenType.AXIOM:
            rule = self.parse_grammar_rule()
            if rule:
                rules.append(rule)
        
        return GrammarSection(rules=rules)
    

    #<GrammarRule>    ::= IDENTIFIER "=" <Alternatives> "\n"
    def parse_grammar_rule(self) -> GrammarRule:
        non_terminal_token = self.consume(TokenType.IDENTIFIER, "Expected non-terminal")
        non_terminal = non_terminal_token.value if non_terminal_token else "<missing>"
        
        self.consume(TokenType.EQUALS, "Expected '=' in grammar rule")
        alternatives = []
        
        alternatives = self.parse_alternatives()

        self.consume(TokenType.SEMICOLON, "Expected ';' after end of rule")
        
        return GrammarRule(
            non_terminal=non_terminal,
            alternatives=alternatives,
        )
    
    #<Alternatives>   ::= <Alternative> ("|" <Alternative>)*
    def parse_alternatives(self) -> List[Alternative]:
        alternatives = []
    
        while True and self.current_token.type:
            sequence = []
        
            sequence =self.parse_sequence()

            
            method_name = None
            if self.current_token and self.current_token.type == TokenType.SLASH:
                self.advance()
                method_name_token = self.consume(TokenType.IDENTIFIER, "Expected method name after '/'",False)
                self.synchronize({TokenType.OR,TokenType.SEMICOLON,TokenType.RPAREN})
                if method_name_token:
                    method_name = method_name_token.value
            alternatives.append(Alternative(elementList=sequence, method_name=method_name))
            if self.current_token and self.current_token.type == TokenType.OR:
                self.advance()
            else: 
                break
       
        return alternatives
    

    #<Sequence> ::= ( <Item> )*
    def parse_sequence(self) -> List[Item]:
        items = []
        
        while self.current_token and self.current_token.type not in {
            TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON, TokenType.RPAREN
        }: 
            item = self.parse_item()
                
            if item:
                items.append(item)
            else:
                self.synchronize({
                   TokenType.OR, TokenType.SLASH, TokenType.SEMICOLON}
                   )
        return items
    
    def parse_group(self) -> Group:
        self.advance()
        alternatives = self.parse_alternatives()
        self.consume(TokenType.RPAREN, "Expected ')' after group")
        return Group(alternatives=alternatives)

    #<Item> ::= <Symbol> | <Group> | <Repetition>
    def parse_item(self) -> Optional[Item]:
        if not self.current_token:
            return None
            
        if self.current_token.type == TokenType.LPAREN:
           return self.parse_group()
            
            
        
        elif self.current_token.type == TokenType.REP:
            self.advance()
            item = []
            if self.current_token.type == TokenType.LPAREN:
                item = self.parse_group()
            else:
                self.add_error(f"Expected group after %rep")
                return None
                
            return Repetition(rep_item=item)
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            
            symbol = Symbol(name=self.current_token.value)
            self.advance()
            
            return symbol
        
        else:
            self.add_error(f"Unexpected item in grammar: {self.current_token.value}")
            self.advance()
            return None
    
   
    
    #<AxiomSection>  ::= "%axiom" IDENTIFIER "\n"
    def parse_axiom_section(self) -> AxiomSection:
        self.consume(TokenType.AXIOM, "Expected '%axiom'")
        axiom_token = self.consume(TokenType.IDENTIFIER, "Expected axiom name")
        axiom = axiom_token.value if axiom_token else "<missing>"
        return AxiomSection(axiom=axiom)
    
    #<EndSection>     ::= "%end" "\n"
    def parse_end_section(self) -> EndSection:
        self.consume(TokenType.END, "Expected '%end'")
        return EndSection()