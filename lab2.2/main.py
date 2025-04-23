import abc
import enum
import parser_edsl as pe
import sys
import typing
from dataclasses import dataclass
from pprint import pprint


class Type(abc.ABC):
    pass

#Type -> int
class TypeEnum(enum.Enum):
    Int = 'int'


@dataclass
class ElementaryType(Type):
    type_: TypeEnum

#TurpleType -> (Type (, Type)*)
@dataclass
class TupleType(Type):
    types: list[Type]


#ListType -> *Type
@dataclass
class ListType(Type):
    type_: Type


class Pattern(abc.ABC):
    pass

#PatternBinary -> Pattern ':' Pattern
@dataclass
class PatternBinary(Pattern):
    lhs: Pattern
    op: str
    rhs: Pattern

#PatternList -> { Pattern (',' Pattern)* }
@dataclass
class PatternList(Pattern):
    patterns: list[Pattern]

#PatternTuple -> '(' Pattern (',' Pattern)* ')'
@dataclass
class PatternTuple(Pattern):
    patterns: list[Pattern]


class Result(abc.ABC):
    pass

#ResultBinary -> Result ':' Result
@dataclass
class ResultBinary(Result):
    lhs: Result
    op: str
    rhs: Result


#ResultList -> { Result (',' Result)* }
@dataclass
class ResultList(Result):
    results: list[Result]

#ResultTuple -> '(' Result (',' Result)* ')'
@dataclass
class ResultTuple(Result):
    results: list[Result]

#VarExpr -> IDENT
@dataclass
class VarExpr(Pattern, Result):
    varname: str

#ConstExpr -> INT
@dataclass
class ConstExpr(Pattern, Result):
    value: typing.Any
    type_: TypeEnum

#FuncCallExpr -> func_name '(' Result ')'
@dataclass
class FuncCallExpr(Result):
    funcname: str
    argument: Result

#Statement -> Pattern '=' Result
@dataclass
class Statement:
    pattern: Pattern
    result: Result

#FuncType -> Type '::' Type
@dataclass
class FuncType:
    input_: Type
    output: Type

#Func -> FuncName FuncType 'is' Statements 'end'
@dataclass
class Func:
    name: str
    type_: FuncType
    body: list[Statement]

#Programm -> Function
@dataclass
class Program:
    funcs: list[Func]


IDENT = pe.Terminal('IDENT', '[A-Za-z_][A-Za-z_0-9]*', str)
INT_CONST = pe.Terminal('INT_CONST', '[0-9]+', int)


def make_keyword(image):
    return pe.Terminal(image, image, lambda _: None, priority=10)


KW_IS, KW_END, KW_INT = map(make_keyword, ['is', 'end', 'int'])

# Основные структуры программы
NProgram, NFuncs, NFunc, NFuncType, NFuncBody = \
    map(pe.NonTerminal, 'Program Funcs Func FuncType FuncBody'.split())

# Типы данных
NType, NElementaryType, NListType, NTupleType, NTupleTypeContent, NTupleTypeItems = \
    map(pe.NonTerminal, 'Type ElementaryType ListType TupleType TupleTypeContent TupleTypeItems'.split())

# Управляющие структуры
NStatements, NStatement = \
    map(pe.NonTerminal, 'Statements Statement'.split())

# Паттерны
NPattern, NConsOp, NPatternUnit, NConst, NPatternList = \
    map(pe.NonTerminal, 'Pattern ConsOp PatternUnit Const PatternList'.split())

# Элементы паттернов
NPatternListContent, NPatternListItems, NPatternListItem = \
    map(pe.NonTerminal, 'PatternListContent PatternListItems PatternListItem'.split())

# Кортежи в паттернах
NPatternTuple, NPatternTupleContent, NPatternTupleItems, NPatternTupleItem = \
    map(pe.NonTerminal, 'PatternTuple PatternTupleContent PatternTupleItems PatternTupleItem'.split())

# Результаты
NResult, NResultUnit = \
    map(pe.NonTerminal, 'Result ResultUnit'.split())

# Выражения
NExpr, NAddOp, NTerm, NMulOp, NFactor, NAtom = \
    map(pe.NonTerminal, 'Expr AddOp Term MulOp Factor Atom'.split())

# Вызовы функций
NFuncCall, NFuncArg = \
    map(pe.NonTerminal, 'FuncCall FuncArg'.split())

# Списки и кортежи в результатах
NResultList, NResultListContent, NResultListItems, NResultListItem = \
    map(pe.NonTerminal, 'ResultList ResultListContent ResultListItems ResultListItem'.split())

NResultTuple, NResultTupleContent, NResultTupleItems, NResultTupleItem = \
    map(pe.NonTerminal, 'ResultTuple ResultTupleContent ResultTupleItems ResultTupleItem'.split())


NProgram |= NFuncs, Program

NFuncs |= lambda: []
NFuncs |= NFuncs, NFunc, lambda fs, f: fs + [f]

NFunc |= IDENT, NFuncType, KW_IS, NFuncBody, KW_END, Func

NFuncType |= NType, '::', NType, FuncType

NType |= NElementaryType
NType |= NListType
NType |= NTupleType

NElementaryType |= KW_INT, lambda: ElementaryType(TypeEnum.Int)

NListType |= '*', NType, ListType

NTupleType |= '(', NTupleTypeContent, ')', TupleType

NTupleTypeContent |= lambda: []
NTupleTypeContent |= NTupleTypeItems

NTupleTypeItems |= NType, lambda t: [t]
NTupleTypeItems |= NTupleTypeItems, ',', NType, lambda ts, t: ts + [t]

NFuncBody |= NStatements

NStatements |= NStatement, lambda s: [s]
NStatements |= NStatements, ';', NStatement, lambda ss, s: ss + [s]

NStatement |= NPattern, '=', NResult, Statement

NPattern |= NPatternUnit
NPattern |= NPatternUnit, NConsOp, NPattern, PatternBinary

NConsOp |= ':', lambda: ':'

NPatternUnit |= IDENT, VarExpr
NPatternUnit |= NConst
NPatternUnit |= NPatternList,
NPatternUnit |= NPatternTuple,
NPatternUnit |= '[', NPattern, ']',

NConst |= INT_CONST, lambda value: ConstExpr(value, TypeEnum.Int)

NPatternList |= '{', NPatternListContent, '}', PatternList

NPatternListContent |= lambda: []
NPatternListContent |= NPatternListItems

NPatternListItems |= NPatternListItem, lambda pli: [pli]
NPatternListItems |= NPatternListItems, ',', NPatternListItem, \
    lambda plis, pli: plis + [pli]

NPatternListItem |= NPattern

NPatternTuple |= '(', NPatternTupleContent, ')', PatternTuple

NPatternTupleContent |= lambda: []
NPatternTupleContent |= NPatternTupleItems

NPatternTupleItems |= NPatternTupleItem, lambda pti: [pti]
NPatternTupleItems |= NPatternTupleItems, ',', NPatternTupleItem, \
    lambda ptis, pti: ptis + [pti]

NPatternTupleItem |= NPattern

NResult |= NResultUnit
NResult |= NResultUnit, NConsOp, NResult, ResultBinary

NResultUnit |= NExpr
NResultUnit |= NResultList,
NResultUnit |= NResultTuple,

NExpr |= NTerm
NExpr |= NExpr, NAddOp, NTerm, ResultBinary

NAddOp |= '+', lambda: '+'
NAddOp |= '-', lambda: '-'

NTerm |= NFactor
NTerm |= NTerm, NMulOp, NFactor, ResultBinary

NMulOp |= '*', lambda: '*'
NMulOp |= '/', lambda: '/'

NFactor |= NAtom
NFactor |= '[', NExpr, ']'

NAtom |= IDENT, VarExpr
NAtom |= NConst
NAtom |= NFuncCall

NFuncCall |= IDENT, NFuncArg, FuncCallExpr

NFuncArg |= NAtom
NFuncArg |= NResultList
NFuncArg |= NResultTuple
NFuncArg |= '[', NResult, ']'

NResultList |= '{', NResultListContent, '}', ResultList

NResultListContent |= lambda: []
NResultListContent |= NResultListItems

NResultListItems |= NResultListItem, lambda rli: [rli]
NResultListItems |= NResultListItems, ',', NResultListItem, \
    lambda rlis, rli: rlis + [rli]

NResultListItem |= NResult

NResultTuple |= '(', NResultTupleContent, ')', ResultTuple

NResultTupleContent |= lambda: []
NResultTupleContent |= NResultTupleItems

NResultTupleItems |= NResultTupleItem, lambda rti: [rti]
NResultTupleItems |= NResultTupleItems, ',', NResultTupleItem, \
    lambda rtis, rti: rtis + [rti]

NResultTupleItem |= NResult

if __name__ == "__main__":
    p = pe.Parser(NProgram)
    assert p.is_lalr_one()

    p.add_skipped_domain('\\s')
    p.add_skipped_domain('@[^\\n]*')

    for filename in sys.argv[1:]:
        try:
            with open(filename) as f:
                pass
                tree = p.parse(f.read())
                pprint(tree)
        except pe.Error as e:
            print(f'Ошибка {e.pos}: {e.message}')
        except Exception as e:
            print(e)