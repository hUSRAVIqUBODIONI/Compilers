from dataclasses import dataclass
from typing import List, Optional, Union

# Базовый класс для всех узлов AST
class ASTNode:
    pass

@dataclass
class Specification(ASTNode):
    class_section: 'ClassSection'
    tokens_section: 'TokensSection'
    types_section: 'TypesSection'
    methods_section: 'MethodsSection'
    grammar_section: 'GrammarSection'
    axiom_section: 'AxiomSection'
    end_section: 'EndSection'
    
    

@dataclass
class ClassSection(ASTNode):
    class_name: str

@dataclass
class TokensSection(ASTNode):
    tokens: List[str]

@dataclass
class TypeDef(ASTNode):
    name: List[str]
    type: str

@dataclass
class TypesSection(ASTNode):
    type_defs: List['TypeDef']


@dataclass
class MethodParam(ASTNode):
    param_type: str

@dataclass
class MethodDecl(ASTNode):
    return_type: str
    method_name: str
    params: List['MethodParam']

@dataclass
class MethodsSection(ASTNode):
    method_decls: List['MethodDecl']

@dataclass
class GrammarRule(ASTNode):
    non_terminal: str
    alternatives: List['Alternative']


@dataclass
class Alternative(ASTNode):
    elementList: List['Item']
    method_name: Optional[str]

@dataclass
class Item(ASTNode):
    pass

@dataclass
class Symbol(Item):
    name: str

@dataclass
class Group(Item):
    alternatives: List['Alternative']

@dataclass
class Repetition(Item):
    rep_item : Group 

@dataclass
class GrammarSection(ASTNode):
    rules: List['GrammarRule']

@dataclass
class AxiomSection(ASTNode):
    axiom: str

@dataclass
class EndSection(ASTNode):
    pass


def print_ast(node: ASTNode, indent: int = 0, prefix: str = "") -> None:
   
    indent_str = " " * indent
    next_indent = indent + 2
    
    if isinstance(node, Specification):
        print(f"{indent_str}{prefix}Specification:")
        print_ast(node.class_section, next_indent, "class_section: ")
        print_ast(node.tokens_section, next_indent, "tokens_section: ")
        print_ast(node.types_section, next_indent, "types_section: ")
        print_ast(node.methods_section, next_indent, "methods_section: ")
        print_ast(node.grammar_section, next_indent, "grammar_section: ")
        print_ast(node.axiom_section, next_indent, "axiom_section: ")
        print_ast(node.end_section, next_indent, "end_section: ")
        
    elif isinstance(node, ClassSection):
        print(f"{indent_str}{prefix}ClassSection(class_name='{node.class_name}')")
    
    elif isinstance(node, AxiomSection):
        print(f"{indent_str}{prefix}AxiomSection(axiom ='{node.axiom}')")

    elif isinstance(node, EndSection):
        print(f"{indent_str}{prefix}EndSection ")
        
    elif isinstance(node, TokensSection):
        print(f"{indent_str}{prefix}TokensSection:")
        for i, token in enumerate(node.tokens):
            print(f"{indent_str}  [{i}]: {token}")
            
    elif isinstance(node, TypeDef):
        print(f"{indent_str}{prefix}TypeDef {node.type}:")
        for i, type_name in enumerate(node.name):
            print(f"{indent_str}  [{i}]: {type_name}")
            
    elif isinstance(node, TypesSection):
        print(f"{indent_str}{prefix}TypesSection:")
        for i, type_def in enumerate(node.type_defs):
            print_ast(type_def, indent + 4, f"[{i}]: ")
            
    elif isinstance(node, MethodParam):
        print(f"{indent_str}{prefix}MethodParam(param_type='{node.param_type}')")
        
    elif isinstance(node, MethodDecl):
        print(f"{indent_str}{prefix}MethodDecl: {node.return_type} {node.method_name}(")
        for i, param in enumerate(node.params):
            print_ast(param, indent + 4, f"param_{i}: ")
        print(f"{indent_str})")
        
    elif isinstance(node, MethodsSection):
        print(f"{indent_str}{prefix}MethodsSection:")
        for i, method_decl in enumerate(node.method_decls):
            print_ast(method_decl, indent + 4, f"[{i}]: ")
    
    elif isinstance(node, GrammarSection):
        print(f"{indent_str}{prefix}GrammarSection:")
        for i, rule in enumerate(node.rules):
            print_ast(rule, indent + 4, f"rule[{i}]: ")
            
    elif isinstance(node, GrammarRule):
        print(f"{indent_str}{prefix}GrammarRule(non_terminal='{node.non_terminal}')")
        for i, alt in enumerate(node.alternatives):
            print_ast(alt, indent + 4, f"alternative[{i}]: ")
            
    elif isinstance(node, Alternative):
        print(f"{indent_str}{prefix}Alternative(method_name={node.method_name or 'None'})")
        for i, item in enumerate(node.elementList):
            print_ast(item, indent + 4, f"element[{i}]")
            
    elif isinstance(node, Symbol):
        print(f"{indent_str}{prefix}Symbol(name='{node.name}')")
        
    elif isinstance(node, Group):
        print(f"{indent_str}{prefix}Group:")
        for i, alt in enumerate(node.alternatives):
            print_ast(alt, indent + 4, f"option[{i}]: ")
            
    elif isinstance(node, Repetition):
        print(f"{indent_str}{prefix}Repetition:")
        print_ast(node.rep_item, indent + 4, "repeated: ")


    else:
        print(f"{indent_str}{prefix}Unknown AST node: {type(node).__name__}")

    
        

  