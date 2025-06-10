import abc
import enum
from abc import ABC

import parser_edsl as pe
from dataclasses import dataclass



class SemanticError(pe.Error, ABC):
    pass


class RepeatedTag(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident

    @property
    def message(self):
        return f'Повторный тег {self.ident}'


class RepeatedField(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident

    @property
    def message(self):
        return f'Повторное поле {self.ident}'


class RepeatedConstant(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident

    @property
    def message(self):
        return f'Повторная константа {self.ident}'


class UnannouncedConstant(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident


    @property
    def message(self):
        return f'Необъявленная константа {self.ident}'

class UnannouncedStruct(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident


    @property
    def message(self):
        return f'Необъявленная структура {self.ident}'

class UnannouncedTag(SemanticError):
    def __init__(self, pos, ident):
        self.pos = pos
        self.ident = ident

    @property
    def message(self):
        return f'Необъявленный тег {self.ident}'


@dataclass
class TypeSpecifier(abc.ABC):
    def check(self):
        pass

    def calculate(self) -> int:
        pass


class SimpleType(enum.Enum):
    Char = "CHAR"
    Short = "SHORT"
    Int = "INT"
    Long = "LONG"
    Float = "FLOAT"
    Double = "DOUBLE"
    Signed = "SIGNED"
    Unsigned = "UNSIGNED"


class Expression(abc.ABC):
    def check(self):
        pass

    def calculate(self, ident) -> int:
        pass


@dataclass
class ConstantExpression:
    expression: Expression

    def check(self):
        pass


@dataclass
class Enumerator:
    identifier: str
    constantExpression: ConstantExpression
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, constExpr = self
        idc, _ = coords
        return Enumerator(ident, constExpr, idc.start)

    def check(self, enum_pos):
        if check_const(self.identifier):
            raise RepeatedConstant(self.identifier_pos, self.identifier)
        if isinstance(self.constantExpression, ConstantExpression):
            add_to_const(self.identifier, self.constantExpression.expression)
            self.constantExpression.expression.check()

        else:
            add_to_const(self.identifier, enum_pos)


@dataclass
class StructOrUnionStatement(abc.ABC):
    def check(self):
        pass

    def calculate_struct_or_union(self) -> int:
        pass


@dataclass
class EmptyStructOrUnionStatement(StructOrUnionStatement):
    identifier: str
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, = self
        idc, = coords
        return EmptyStructOrUnionStatement(ident, idc.start)

    def check(self, _):
        if self.identifier not in esu_tag:
            raise UnannouncedTag(self.identifier_pos, self.identifier)
        
    
    def calculate_struct_or_union(self, _) -> int:
        
        
        o = esu_tag[self.identifier]
       
        if isinstance(o, StructOrUnionSpecifier):
            if self.identifier in calculated_sized:
                return calculated_sized[self.identifier]
            else:
                return 4
        else:
            raise ValueError(f'Obj {o} is not StructOrUnionSpecifier')


@dataclass
class StructOrUnionSpecifier(TypeSpecifier):
    type: str
    structOrUnionSpecifier: StructOrUnionStatement

    def check(self):
        self.structOrUnionSpecifier.check(self.type)

    def calculate(self) -> int:
        return self.structOrUnionSpecifier.calculate_struct_or_union(self.type)


@dataclass
class EnumStatement(abc.ABC):
    def check(self):
        pass

    def calculate(self) -> int:
        pass


@dataclass
class EnumTypeSpecifier(TypeSpecifier):
    enumStatement: EnumStatement

    def check(self):
        self.enumStatement.check()

    def calculate(self) -> int:
        return self.enumStatement.calculate()


@dataclass
class FullEnumStatement(EnumStatement):
    identifier: str
    enumeratorList: list[Enumerator]
    isEndComma: bool
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, enList, IsComma = self
        idc, _, enc, _, icc = coords
        return FullEnumStatement(ident, enList, IsComma, idc.start)

    def check(self):
        if len(self.identifier) != 0 and check_and_add_to_map(self.identifier, self):
            raise RepeatedTag(self.identifier_pos, self.identifier)

        for idx, enumerator in enumerate(self.enumeratorList):
            enumerator.check(idx)

    def calculate(self) -> int:
        return 4


@dataclass
class EmptyEnumStatement(EnumStatement):
    identifier: str
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, = self
        idc, = coords
        return EmptyEnumStatement(ident, idc.start)

    def check(self):
        if self.identifier not in esu_tag:
            raise UnannouncedTag(self.identifier_pos, self.identifier)

    def calculate(self) -> int:
        return 4


@dataclass
class IdentifierExpression(Expression):
    identifier: str
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, = self
        idc, = coords
        return IdentifierExpression(ident, idc.start)

    def check(self):
        if not check_const(self.identifier):
            raise UnannouncedConstant(self.identifier_pos, self.identifier)

    def calculate(self, ident) -> int:
        if self.identifier in calculated_expr:
            return int(calculated_expr[self.identifier])
        else:
            raise ValueError(f'Identifier {self.identifier} not found in calculate_const')


@dataclass
class IntExpression(Expression):
    value: int

    def check(self):
        pass

    def calculate(self, ident) -> int:
        calculated_expr[ident] = int(self.value)
        return int(self.value)


@dataclass
class BinaryOperationExpression(Expression):
    left: Expression
    operation: str
    right: Expression

    def check(self):
        self.left.check()
        self.right.check()

    def calculate(self, ident) -> int:
        if self.operation == '+':
            return self.left.calculate(ident) + self.right.calculate(ident)
        elif self.operation == '-':
            return self.left.calculate(ident) - self.right.calculate(ident)
        elif self.operation == '*':
            return self.left.calculate(ident) * self.right.calculate(ident)
        elif self.operation == '/':
            return self.left.calculate(ident) // self.right.calculate(ident)
        else:
            raise ValueError("Unsupported operation in BinaryOperationExpression", self.operation)


@dataclass
class UnaryOperationExpression(Expression):
    operation: str
    expression: Expression

    def check(self):
        self.expression.check()

    def calculate(self, ident) -> int:
        if self.operation == '+':
            return self.expression.calculate(ident)
        elif self.operation == '-':
            return -self.expression.calculate(ident)
        else:
            raise ValueError("Unsupported operation in UnaryOperationExpression", self.operation)


@dataclass
class ListArraysOpt:
    listArraysOpt: list[str]


@dataclass
class AbstractDeclarator(abc.ABC):
    def check(self, field_name):
        pass

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        pass


@dataclass
class AbstractDeclaratorPointer(AbstractDeclarator):
    declarator: AbstractDeclarator

    def check(self, field_name):
        self.declarator.check(field_name)

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        count, _ = self.declarator.calculate_abstract_and_get_pointer_info()
        return count, True


@dataclass
class AbstractDeclaratorArrayList:
    arrays: list[AbstractDeclarator]

    def check(self, field_name):
        for ad in self.arrays:
            ad.check(field_name)

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        multy = 1
        for a in self.arrays:
            p, _ = a.calculate_abstract_and_get_pointer_info()
            multy *= p
        return multy, False


@dataclass
class AbstractDeclaratorArray(AbstractDeclarator):
    size_of_array: Expression

    def check(self, _):
        self.size_of_array.check()

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        calc = self.size_of_array.calculate("")
        return calc, False


@dataclass
class AbstractDeclaratorsOpt:
    abstractDeclaratorList: list[AbstractDeclarator]

    def check(self, field_name):
        for ad in self.abstractDeclaratorList:
            ad.check(field_name)

    def calculate_abstract(self) -> int:
        summer = 0
        for ad in self.abstractDeclaratorList:
            calc, _ = ad.calculate_abstract_and_get_pointer_info()
            summer += calc
        return summer


@dataclass
class SimpleTypeSpecifier(TypeSpecifier):
    simpleType: SimpleType

    def check(self):
        pass

    def calculate(self) -> int:
        if self.simpleType in [SimpleType.Int, SimpleType.Float,
                               SimpleType.Long, SimpleType.Short]:
            return 4
        elif self.simpleType == SimpleType.Double:
            return 8
        else:
            return 1


calculated_sized = {}


@dataclass
class SizeofExpression(Expression):
    typeName: str
    identName: str
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        typeName, identName = self
        _, _, _, idc, _ = coords
        return SizeofExpression(typeName, identName, idc.start)

    def check(self):
        if self.identName not in esu_tag:
            raise UnannouncedTag(self.identifier_pos, self.identName)

    def calculate(self, ident) -> int:
        decl = esu_tag[self.identName]
        if isinstance(decl, StructOrUnionSpecifier):
            struct_or_union_specifier_obj = decl
            if self.typeName != struct_or_union_specifier_obj.type:
                raise ValueError(f"Incorrect type of sizeof expression,"
                                 f" expected: {self.typeName},"
                                 f" got: {struct_or_union_specifier_obj.type} in", self)
            if ident in calculated_sized:
                return calculated_sized[ident]
            else:
                s_size = struct_or_union_specifier_obj.calculate()
                calculated_sized[ident] = s_size
                return s_size
        elif isinstance(decl, FullEnumStatement):
            enum_statement_obj = decl
            if self.typeName != "enum":
                raise ValueError("Incorrect type of sizeof expression", self.typeName, "enum")
            return enum_statement_obj.calculate()
        else:
            raise ValueError("Incorrect type of sizeof expression", self.typeName, "enum")


@dataclass
class Declaration:
    declarationBody: TypeSpecifier
    varName: AbstractDeclaratorsOpt

    def check(self, field_name):
        self.varName.check(field_name)
        self.declarationBody.check()

    def calculate(self) -> int:
        abstract = self.varName.calculate_abstract()
        return self.declarationBody.calculate() * abstract


@dataclass
class AbstractDeclaratorPrim(abc.ABC):
    pass

    def calculate_ident_and_get_pointer_info(self) -> int:
        pass


@dataclass
class AbstractDeclaratorPrimSimple(AbstractDeclaratorPrim):
    identifier: str
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, = self
        idc, = coords
        return AbstractDeclaratorPrimSimple(ident, idc.start)

    def check(self, field_name):
        if self.identifier in field_name:
            raise RepeatedField(self.identifier_pos, self.identifier)
        field_name.append(self.identifier)

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        if self.identifier != "":
            pass
        return 1, False


@dataclass
class AbstractDeclaratorPrimDifficult(AbstractDeclaratorPrim):
    identifier: AbstractDeclarator

    def check(self, field_name):
        self.identifier.check(field_name)

    def calculate_abstract_and_get_pointer_info(self) -> (int, bool):
        return self.identifier.calculate_abstract_and_get_pointer_info()


@dataclass
class FullStructOrUnionStatement(StructOrUnionStatement):
    identifierOpt: str
    declarationList: list[Declaration]
    identifier_pos: pe.Position

    @pe.ExAction
    def create(self, coords, res_coord):
        ident, declList = self
        idc, _, dc, _ = coords
        return FullStructOrUnionStatement(ident, declList, idc.start)

    def check(self, type_obj):
        field_name = list()

        if (len(self.identifierOpt) != 0 and
                check_and_add_to_map(self.identifierOpt, StructOrUnionSpecifier(type_obj, self))):
            raise RepeatedTag(self.identifier_pos, self.identifierOpt)

        for declaration in self.declarationList:
            declaration.check(field_name)

    def calculate_struct_or_union(self, type_obj) -> int:
       
        summer = 0
        if self.identifierOpt != "":
            if self.identifierOpt in calculated_sized:
                return calculated_sized[self.identifierOpt]
            else:
                if type_obj == "struct":
                    for d in self.declarationList:
                        summer += d.calculate()
                    calculated_sized[self.identifierOpt] = summer
                   
                    return summer
                else:
                    temp =0
                    for d in self.declarationList:
                        for i, decls in esu_tag.items():
                            if d.declarationBody.structOrUnionSpecifier.identifier == i:
                                temp = decls.calculate()
                        summer = max(temp, summer)
                    calculated_sized[self.identifierOpt] = summer
                    return summer

        if type_obj == "struct":
            for d in self.declarationList:
                summer += d.calculate()
        else:
            for d in self.declarationList:
                summer = max(d.calculate(), summer)
        return summer


esu_tag = {}


def check_and_add_to_map(s, decl):
    if s in esu_tag:
        return True
    else:
        esu_tag[s] = decl
        return False


const_name = {}


def check_const(ident):
    return ident in const_name


def add_to_const(ident, expr):
    const_name[ident] = expr


@dataclass
class Program:
    declarationList: list[Declaration]

    def check(self):
        for declaration in self.declarationList:
            field_name = list()
            declaration.check(field_name)


NProgram = pe.NonTerminal('Program')

NDeclarationList = pe.NonTerminal('DeclarationList')
NDeclaration = pe.NonTerminal('Declaration')

NAbstractDeclaratorsOpt = pe.NonTerminal('AbstractDeclaratorsOpt')
NAbstractDeclarators = pe.NonTerminal('AbstractDeclarators')
NAbstractDeclarator = pe.NonTerminal('AbstractDeclarator')

NAbstractDeclaratorStar = pe.NonTerminal('AbstractDeclaratorStar')

NAbstractDeclaratorArrayList = pe.NonTerminal('AbstractDeclaratorArrayList')

NAbstractDeclaratorArray = pe.NonTerminal('AbstractDeclaratorArray')

NAbstractDeclaratorPrim = pe.NonTerminal('AbstractDeclaratorPrim')

NAbstractDeclaratorPrimSimple = pe.NonTerminal('AbstractDeclaratorPrimSimple')
NAbstractDeclaratorPrimDifficult = pe.NonTerminal('AbstractDeclaratorPrimDifficult')

NTypeSpecifier = pe.NonTerminal('TypeSpecifier')

NEnumTypeSpecifier = pe.NonTerminal('EnumTypeSpecifier')

NSimpleTypeSpecifier = pe.NonTerminal('SimpleTypeSpecifier')
NSimpleType = pe.NonTerminal('SimpleType')

NEnumStatement = pe.NonTerminal('EnumStatement')

NFullEnumStatement = pe.NonTerminal('FullEnumStatement')
NEmptyEnumStatement = pe.NonTerminal('EmptyEnumStatement')

NEnumeratorList = pe.NonTerminal('EnumeratorList')
NEnumerator = pe.NonTerminal('Enumerator')

NEnumeratorExpressionOpt = pe.NonTerminal('EnumeratorExpressionOpt')
NConstantExpression = pe.NonTerminal('ConstantExpression')

NIdentifierOpt = pe.NonTerminal('IdentifierOpt')

NCommaOpt = pe.NonTerminal('CommaOpt')

NExpression = pe.NonTerminal('Expression')

NArithmeticExpression = pe.NonTerminal('ArithmeticExpression')
NTerm = pe.NonTerminal('Term')
NAddOperation = pe.NonTerminal('AddOperation')

NFactor = pe.NonTerminal('Factor')
NMultyOperation = pe.NonTerminal('MultyOperation')

NStructOrUnionSpecifier = pe.NonTerminal('StructOrUnionSpecifier')

NStructOrUnion = pe.NonTerminal('StructOrUnion')

NStructOrUnionStatement = pe.NonTerminal('StructOrUnionStatement')

NFullStructOrUnionStatement = pe.NonTerminal('FullStructOrUnionStatement')
NEmptyStructOrUnionStatement = pe.NonTerminal('EmptyStructOrUnionStatement')

NTypeSizeofSpecifier = pe.NonTerminal('TypeSizeofSpecifier')


def make_keyword(image):
    return pe.Terminal(image, image, lambda _: None, priority=10)


KW_ENUM = make_keyword('enum')
KW_STRUCT = make_keyword('struct')
KW_UNION = make_keyword('union')

KW_SIZEOF = make_keyword('sizeof')

KW_CHAR, KW_SHORT, KW_INT, KW_LONG, KW_FLOAT, KW_DOUBLE, KW_SIGNED, KW_UNSIGNED = \
    map(make_keyword, 'char short int long float double signed unsigned'.split())

INTEGER = pe.Terminal('IDENTIFIER', r'[0-9]*', str)

IDENTIFIER = pe.Terminal('IDENTIFIER', r'[A-Za-z_]([A-Za-z_0-9])*', str)

NProgram |= NDeclarationList, Program

NDeclarationList |= lambda: []
NDeclarationList |= NDeclarationList, NDeclaration, lambda dl, d: dl + [d]

NDeclaration |= NTypeSpecifier, NAbstractDeclaratorsOpt, ';', Declaration

NAbstractDeclaratorsOpt |= lambda: AbstractDeclaratorsOpt(list())
NAbstractDeclaratorsOpt |= NAbstractDeclarators, AbstractDeclaratorsOpt

NAbstractDeclarators |= NAbstractDeclarator, lambda a: [a]
NAbstractDeclarators |= NAbstractDeclarators, ',', NAbstractDeclarator, lambda ads, a: ads + [a]

NAbstractDeclarator |= NAbstractDeclaratorStar, AbstractDeclaratorPointer
NAbstractDeclarator |= NAbstractDeclaratorArrayList, AbstractDeclaratorArrayList

NAbstractDeclaratorStar |= '*', NAbstractDeclarator, AbstractDeclaratorPointer

NAbstractDeclaratorArrayList |= NAbstractDeclaratorArray, lambda a: [a]
NAbstractDeclaratorArrayList |= (NAbstractDeclaratorArrayList, NAbstractDeclaratorArray,
                                 lambda adal, a: adal + [a])

NAbstractDeclaratorArray |= '[', NExpression, ']', AbstractDeclaratorArray

NAbstractDeclaratorArray |= NAbstractDeclaratorPrim
NAbstractDeclaratorPrim |= NAbstractDeclaratorPrimSimple, AbstractDeclaratorPrimSimple.create

NAbstractDeclaratorPrim |= NAbstractDeclaratorPrimDifficult, AbstractDeclaratorPrimDifficult

NAbstractDeclaratorPrimSimple |= IDENTIFIER

NAbstractDeclaratorPrimDifficult |= '(', NAbstractDeclarator, ')'

NTypeSpecifier |= NEnumTypeSpecifier
NTypeSpecifier |= NSimpleTypeSpecifier
NTypeSpecifier |= NStructOrUnionSpecifier

NSimpleTypeSpecifier |= NSimpleType, SimpleTypeSpecifier

NSimpleType |= KW_CHAR, lambda: SimpleType.Char
NSimpleType |= KW_SHORT, lambda: SimpleType.Short
NSimpleType |= KW_INT, lambda: SimpleType.Int
NSimpleType |= KW_LONG, lambda: SimpleType.Long
NSimpleType |= KW_FLOAT, lambda: SimpleType.Float
NSimpleType |= KW_DOUBLE, lambda: SimpleType.Double
NSimpleType |= KW_SIGNED, lambda: SimpleType.Signed
NSimpleType |= KW_UNSIGNED, lambda: SimpleType.Unsigned

NEnumTypeSpecifier |= KW_ENUM, NEnumStatement, EnumTypeSpecifier

NEnumStatement |= NFullEnumStatement

NFullEnumStatement |= NIdentifierOpt, '{', NEnumeratorList, NCommaOpt, '}', FullEnumStatement.create

NIdentifierOpt |= lambda: ""
NIdentifierOpt |= IDENTIFIER

NEnumStatement |= NEmptyEnumStatement, EmptyEnumStatement.create

NEmptyEnumStatement |= IDENTIFIER

NEnumeratorList |= NEnumerator, lambda e: [e]
NEnumeratorList |= NEnumeratorList, ',', NEnumerator, lambda el, e: el + [e]

NEnumerator |= IDENTIFIER, NEnumeratorExpressionOpt, Enumerator.create

NEnumeratorExpressionOpt |= '=', NConstantExpression, ConstantExpression
NEnumeratorExpressionOpt |= lambda: ""

NCommaOpt |= ',', lambda: True
NCommaOpt |= lambda: False

NConstantExpression |= NExpression

NExpression |= NArithmeticExpression

NArithmeticExpression |= NTerm
NArithmeticExpression |= '+', NTerm, lambda t: UnaryOperationExpression('+', t)
NArithmeticExpression |= '-', NTerm, lambda t: UnaryOperationExpression('-', t)
NArithmeticExpression |= NArithmeticExpression, NAddOperation, NTerm, BinaryOperationExpression

NAddOperation |= '+', lambda: '+'
NAddOperation |= '-', lambda: '-'

NTerm |= NFactor
NTerm |= NTerm, NMultyOperation, NFactor, BinaryOperationExpression

NMultyOperation |= '*', lambda: '*'
NMultyOperation |= '/', lambda: '/'

NFactor |= '(', NExpression, ')'

NFactor |= INTEGER, IntExpression

NFactor |= IDENTIFIER, IdentifierExpression.create

NFactor |= KW_SIZEOF, '(', NTypeSizeofSpecifier, IDENTIFIER, ')', SizeofExpression.create

NStructOrUnionSpecifier |= NStructOrUnion, NStructOrUnionStatement, StructOrUnionSpecifier

NStructOrUnion |= KW_STRUCT, lambda: "struct"
NStructOrUnion |= KW_UNION, lambda: "union"

NTypeSizeofSpecifier |= KW_STRUCT, lambda: "struct"
NTypeSizeofSpecifier |= KW_UNION, lambda: "union"
NTypeSizeofSpecifier |= KW_ENUM, lambda: "enum"

NStructOrUnionStatement |= NFullStructOrUnionStatement
NStructOrUnionStatement |= NEmptyStructOrUnionStatement

NEmptyStructOrUnionStatement |= IDENTIFIER, EmptyStructOrUnionStatement.create

NFullStructOrUnionStatement |= NIdentifierOpt, '{', NDeclarationList, '}', FullStructOrUnionStatement.create


def main():
    p = pe.Parser(NProgram)

    assert p.is_lalr_one()

    p.add_skipped_domain('\\s')


    filename = "test.txt"


    
    print("file:", filename)
    try:
        with open(filename) as f:
            tree = p.parse(f.read())
            tree.check()
            print("Семантических ошибок не найдено")
    except pe.Error as e:
        print(f'Ошибка {e.pos}: {e.message}')
    except Exception as e:
        print(e)


calculated_expr = {}


def calculate_constant():
    for ident, expr in const_name.items():
        if hasattr(expr, 'calculate') and callable(getattr(expr, 'calculate')):
            calculated_expr[ident] = expr.calculate(ident)
        else:
            calculated_expr[ident] = expr


calculated_capacity = {}


def calculate_capacity():
   
    for ident, decls in esu_tag.items():
       
        if hasattr(decls, 'calculate') and callable(getattr(decls, 'calculate')):
            try:
                calculated_capacity[ident] = decls.calculate()
            except:
                return
            
        else:
            raise ValueError("Unsupported sizeof for object", ident, decls)


def print_constant():
    print("CONSTANTS:")
    for ident, expr in calculated_expr.items():
        print(f'{ident}: {expr}')
    print()


def print_capacity():
    print("CAPACITY:")
    for ident, expr in calculated_capacity.items():
        print(f'{ident}: {expr}')
    print()


main()

calculate_constant()
print_constant()

calculate_capacity()
print_capacity()