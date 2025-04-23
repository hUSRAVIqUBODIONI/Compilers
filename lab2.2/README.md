% Лабораторная работа № 2.2 «Абстрактные синтаксические деревья»
% 22 апреля 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
    
Целью данной работы является получение навыков составления грамматик и проектирования
синтаксических деревьев.

# Индивидуальный вариант
```
Статически типизированный функциональный язык программирования с сопоставлением с образцом:

 @ Объединение двух списков
zip (*int, *int) :: *(int, int) is
  (x : xs, y : ys) = (x, y) : zip (xs, ys);
  (xs, ys) = {}
end

@ Декартово произведение
cart_prod (*int, *int) :: *(int, int) is
  (x : xs, ys) = append (bind (x, ys), cart_prod(xs, ys));
  ({}, ys) = {}
end

bind (int, *int) :: *(int, int) is
  (x, {}) = {};
  (x, y : ys) = (x, y) : bind (x, ys)
end

@ Конкатенация списков пар
append (*(int, int), *(int, int)) :: *(int, int) is
  (x : xs, ys) = x : append (xs, ys);
  ({}, ys) = ys
end

@ Расплющивание вложенного списка
flat **int :: *int is
  [x : xs] : xss = x : flat [xs : xss];
  {} : xss = flat xss;
  {} = {}
end

@ Сумма элементов списка
sum *int :: int is
  x : xs = x + sum xs;
  {} = 0
end

@ Вычисление полинома по схеме Горнера
polynom (int, *int) :: int is
  (x, {}) = 0;
  (x, coef : coefs) = polynom (x, coefs) * x + coef
end

@ Вычисление полинома x³+x²+x+1
polynom1111 int :: int is x = polynom (x, {1, 1, 1, 1}) end
Комментарии начинаются на знак @.

Все функции в рассматриваемом языке являются функциями одного аргумента. Когда нужно вызвать функцию с
несколькими аргументами, они передаются в виде кортежа.

Круглые скобки служат для создания кортежа, фигурные — для создания списка, квадратные — для указания
приоритета.

Наивысший приоритет имеет операция вызова функции. Вызов функции правоассоциативен, т.е. выражение x y z
трактуется как x [y z] (аргументом функции y является z, аргументом функции x — выражение y z.

За вызовом функции следуют арифметические операции *, /, +, - с обычным приоритетом
(у * и / он выше, чем у + и -) и ассоциативностью (левая).

Наинизшим приоритетом обладает операция создания cons-ячейки :, ассоциативность — правая
(т.е. x : y : z трактуется как x : [y : z]).

Функция состоит из заголовка, в котором указывается её тип, и тела, содержащего несколько
предложений. Предложения разделяются знаком ;.

Предложение состоит из образца и выражения, разделяемых знаком =. В образце, в отличие от выражения,
недопустимы арифметические операции и вызовы функций.

Тип списка описывается с помощью одноместной операции *, предваряющей тип, тип кортежа — как 
перечисление типов элементов через запятую в круглых скобках.

Ключевые слова и идентификаторы чувствительны к регистру.
```

# Реализация

## Абстрактный синтаксис
```
Program -> Function*
Function -> FuncName Arg '::' Return 'is' Body+ 'end'
Arg -> Type
Return -> Type
Body -. Pattern '=' Expression
Pattern -> ID | {} | TuplePattern | Список | Квадрат | ConsPattern
TuplePattern -> '(' Pattern (',' Pattern)* ')'
Список -> '{' Pattern (',' Pattern)* '}'
Квадрат -> '[' Pattern ']'
ConsPattern -> Pattern ':' Pattern

Expression -> ID | {} | TupleExpression | СписокExpr | КвадратExpr | ConsExpr| ArifOp| Num
ArifOp -> Expresion (+|-|/|*) Expression
TupleExpression -> '(' Expresion (',' Expresion)* ')'
СписокExpr -> '{' Expresion (',' Expresion)* '}'
КвадратExpr -> '[' Expression ']'
ConsExpr -> Expression ':' Expression

Type -> BaseType | ListType | TupleType
BaseType -> INT
ListType -> '*'Type
TupleType -> '(' Type (',' Type )* ')'
ID -> (?|\d)\w*
FuncName -> ID
```

## Лексическая структура и конкретный синтаксис
```
Program      ::= Function*
Function     ::= '@' Comment? Name Signature 'is' Clause* 'end'
Comment      ::= '@' [^\n]*
Name         ::= Identifier
Signature    ::= '(' ParamTypes? ')' '::' Type
ParamTypes   ::= Type (',' Type)*
Type         ::= 
               | BasicType
               | ListType
               | TupleType
BasicType    ::= 'int' | 'bool' | 'char' | Identifier
ListType     ::= '*' Type
TupleType    ::= '(' Type (',' Type)+ ')'
Clause       ::= Pattern '=' Expr ';'
Pattern      ::= 
               | TuplePattern
               | ListPattern
               | ConsPattern
               | EmptyListPattern
               | VariablePattern
TuplePattern ::= '(' Pattern (',' Pattern)+ ')'
ListPattern  ::= '[' Pattern (',' Pattern)* ']'
ConsPattern  ::= Identifier ':' Identifier
EmptyListPattern ::= '{}'
VariablePattern ::= Identifier
Expr         ::= 
               | Literal
               | Variable
               | TupleExpr
               | ListExpr
               | ConsExpr
               | FunctionCall
               | BinaryOp
               | ParenExpr
Literal      ::= IntLiteral | BoolLiteral | CharLiteral | EmptyListLiteral
Variable     ::= Identifier
TupleExpr    ::= '(' Expr (',' Expr)+ ')'
ListExpr     ::= '{' Expr (',' Expr)* '}'
ConsExpr     ::= Expr ':' Expr
FunctionCall ::= Identifier '(' Expr (',' Expr)* ')'
BinaryOp     ::= Expr Operator Expr
Operator     ::= '+' | '-' | '*' | '/' | '&&' | '||' | ...
ParenExpr    ::= '(' Expr ')'
```

## Программная реализация

```python

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
```

# Тестирование

## Входные данные

```
@ Объединение двух списков
zip (*int, *int) :: *(int, int) is
  (x : xs, y : ys) = (x, y) : zip (xs, ys);
  (xs, ys) = {}
end

@ Декартово произведение
cart_prod (*int, *int) :: *(int, int) is
  (x : xs, ys) = append (bind (x, ys), cart_prod(xs, ys));
  ({}, ys) = {}
end

bind (int, *int) :: *(int, int) is
  (x, {}) = {};
  (x, y : ys) = (x, y) : bind (x, ys)
end

@ Конкатенация списков пар
append (*(int, int), *(int, int)) :: *(int, int) is
  (x : xs, ys) = x : append (xs, ys);
  ({}, ys) = ys
end

@ Расплющивание вложенного списка
flat **int :: *int is
  [x : xs] : xss = x : flat [xs : xss];
  {} : xss = flat xss;
  {} = {}
end

@ Сумма элементов списка
sum *int :: int is
  x : xs = x + sum xs;
  {} = 0
end

@ Вычисление полинома по схеме Горнера
polynom (int, *int) :: int is
  (x, {}) = 0;
  (x, coef : coefs) = polynom (x, coefs) * x + coef
end

@ Вычисление полинома x³+x²+x+1
polynom1111 int :: int is x = polynom (x, {1, 1, 1, 1}) end
```

## Вывод на `stdout`

<!-- ENABLE LONG LINES -->

```
Program(funcs=[Func(name='zip',
                    type_=FuncType(input_=TupleType(types=[ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                                                           ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))]),
                                   output=ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                          ElementaryType(type_=<TypeEnum.Int: 'int'>)]))),
                    body=[Statement(pattern=PatternTuple(patterns=[PatternBinary(lhs=VarExpr(varname='x'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='xs')),
                                                                   PatternBinary(lhs=VarExpr(varname='y'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='ys'))]),
                                    result=ResultBinary(lhs=ResultTuple(results=[VarExpr(varname='x'),
                                                                                 VarExpr(varname='y')]),
                                                        op=':',
                                                        rhs=FuncCallExpr(funcname='zip',
                                                                         argument=ResultTuple(results=[VarExpr(varname='xs'),
                                                                                                       VarExpr(varname='ys')])))),
                          Statement(pattern=PatternTuple(patterns=[VarExpr(varname='xs'),
                                                                   VarExpr(varname='ys')]),
                                    result=ResultList(results=[]))]),
               Func(name='cart_prod',
                    type_=FuncType(input_=TupleType(types=[ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                                                           ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))]),
                                   output=ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                          ElementaryType(type_=<TypeEnum.Int: 'int'>)]))),
                    body=[Statement(pattern=PatternTuple(patterns=[PatternBinary(lhs=VarExpr(varname='x'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='xs')),
                                                                   VarExpr(varname='ys')]),
                                    result=FuncCallExpr(funcname='append',
                                                        argument=ResultTuple(results=[FuncCallExpr(funcname='bind',
                                                                                                   argument=ResultTuple(results=[VarExpr(varname='x'),
                                                                                                                                 VarExpr(varname='ys')])),
                                                                                      FuncCallExpr(funcname='cart_prod',
                                                                                                   argument=ResultTuple(results=[VarExpr(varname='xs'),
                                                                                                                                 VarExpr(varname='ys')]))]))),
                          Statement(pattern=PatternTuple(patterns=[PatternList(patterns=[]),
                                                                   VarExpr(varname='ys')]),
                                    result=ResultList(results=[]))]),
               Func(name='bind',
                    type_=FuncType(input_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                           ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))]),
                                   output=ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                          ElementaryType(type_=<TypeEnum.Int: 'int'>)]))),
                    body=[Statement(pattern=PatternTuple(patterns=[VarExpr(varname='x'),
                                                                   PatternList(patterns=[])]),
                                    result=ResultList(results=[])),
                          Statement(pattern=PatternTuple(patterns=[VarExpr(varname='x'),
                                                                   PatternBinary(lhs=VarExpr(varname='y'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='ys'))]),
                                    result=ResultBinary(lhs=ResultTuple(results=[VarExpr(varname='x'),
                                                                                 VarExpr(varname='y')]),
                                                        op=':',
                                                        rhs=FuncCallExpr(funcname='bind',
                                                                         argument=ResultTuple(results=[VarExpr(varname='x'),
                                                                                                       VarExpr(varname='ys')]))))]),
               Func(name='append',
                    type_=FuncType(input_=TupleType(types=[ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                                           ElementaryType(type_=<TypeEnum.Int: 'int'>)])),
                                                           ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                                           ElementaryType(type_=<TypeEnum.Int: 'int'>)]))]),
                                   output=ListType(type_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                                          ElementaryType(type_=<TypeEnum.Int: 'int'>)]))),
                    body=[Statement(pattern=PatternTuple(patterns=[PatternBinary(lhs=VarExpr(varname='x'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='xs')),
                                                                   VarExpr(varname='ys')]),
                                    result=ResultBinary(lhs=VarExpr(varname='x'),
                                                        op=':',
                                                        rhs=FuncCallExpr(funcname='append',
                                                                         argument=ResultTuple(results=[VarExpr(varname='xs'),
                                                                                                       VarExpr(varname='ys')])))),
                          Statement(pattern=PatternTuple(patterns=[PatternList(patterns=[]),
                                                                   VarExpr(varname='ys')]),
                                    result=VarExpr(varname='ys'))]),
               Func(name='flat',
                    type_=FuncType(input_=ListType(type_=ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))),
                                   output=ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))),
                    body=[Statement(pattern=PatternBinary(lhs=PatternBinary(lhs=VarExpr(varname='x'),
                                                                            op=':',
                                                                            rhs=VarExpr(varname='xs')),
                                                          op=':',
                                                          rhs=VarExpr(varname='xss')),
                                    result=ResultBinary(lhs=VarExpr(varname='x'),
                                                        op=':',
                                                        rhs=FuncCallExpr(funcname='flat',
                                                                         argument=ResultBinary(lhs=VarExpr(varname='xs'),
                                                                                               op=':',
                                                                                               rhs=VarExpr(varname='xss'))))),
                          Statement(pattern=PatternBinary(lhs=PatternList(patterns=[]),
                                                          op=':',
                                                          rhs=VarExpr(varname='xss')),
                                    result=FuncCallExpr(funcname='flat',
                                                        argument=VarExpr(varname='xss'))),
                          Statement(pattern=PatternList(patterns=[]),
                                    result=ResultList(results=[]))]),
               Func(name='sum',
                    type_=FuncType(input_=ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                                   output=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                    body=[Statement(pattern=PatternBinary(lhs=VarExpr(varname='x'),
                                                          op=':',
                                                          rhs=VarExpr(varname='xs')),
                                    result=ResultBinary(lhs=VarExpr(varname='x'),
                                                        op='+',
                                                        rhs=FuncCallExpr(funcname='sum',
                                                                         argument=VarExpr(varname='xs')))),
                          Statement(pattern=PatternList(patterns=[]),
                                    result=ConstExpr(value=0,
                                                     type_=<TypeEnum.Int: 'int'>))]),
               Func(name='polynom',
                    type_=FuncType(input_=TupleType(types=[ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                                           ListType(type_=ElementaryType(type_=<TypeEnum.Int: 'int'>))]),
                                   output=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                    body=[Statement(pattern=PatternTuple(patterns=[VarExpr(varname='x'),
                                                                   PatternList(patterns=[])]),
                                    result=ConstExpr(value=0,
                                                     type_=<TypeEnum.Int: 'int'>)),
                          Statement(pattern=PatternTuple(patterns=[VarExpr(varname='x'),
                                                                   PatternBinary(lhs=VarExpr(varname='coef'),
                                                                                 op=':',
                                                                                 rhs=VarExpr(varname='coefs'))]),
                                    result=ResultBinary(lhs=ResultBinary(lhs=FuncCallExpr(funcname='polynom',
                                                                                          argument=ResultTuple(results=[VarExpr(varname='x'),
                                                                                                                        VarExpr(varname='coefs')])),
                                                                         op='*',
                                                                         rhs=VarExpr(varname='x')),
                                                        op='+',
                                                        rhs=VarExpr(varname='coef')))]),
               Func(name='polynom1111',
                    type_=FuncType(input_=ElementaryType(type_=<TypeEnum.Int: 'int'>),
                                   output=ElementaryType(type_=<TypeEnum.Int: 'int'>)),
                    body=[Statement(pattern=VarExpr(varname='x'),
                                    result=FuncCallExpr(funcname='polynom',
                                                        argument=ResultTuple(results=[VarExpr(varname='x'),
                                                                                      ResultList(results=[ConstExpr(value=1,
                                                                                                                    type_=<TypeEnum.Int: 'int'>),
                                                                                                          ConstExpr(value=1,
                                                                                                                    type_=<TypeEnum.Int: 'int'>),
                                                                                                          ConstExpr(value=1,
                                                                                                                    type_=<TypeEnum.Int: 'int'>),
                                                                                                          ConstExpr(value=1,
                                                                                                                    type_=<TypeEnum.Int: 'int'>)])])))])])

```

# Вывод
Во время выполнения работы мне понравилось, что можно сосредоточиться на описании грамматики, а библиотека 
parser_edsl.py автоматически строит парсер. Это удобно, потому что не нужно вручную писать разбор токенов 
и синтаксических правил — достаточно правильно задать структуру языка, и система сама генерирует анализатор.

Также было интересно проектировать абстрактное синтаксическое дерево (AST) с помощью дата-классов Python. 
Это делает код чище и понятнее, а автоматическая генерация __init__, __repr__ и других методов экономит 
время.

Меня приятно удивил тот факт, что библиотеку parser_edsl.py, которую мы использовали в работе, разработали 
студенты нашей кафедры. Это показывает высокий уровень подготовки и практическую пользу знаний, которые 
здесь дают.

Было интересно работать с инструментом, созданным «в стенах» нашего вуза, и видеть, как он упрощает 
написание парсеров. Это вдохновляет и мотивирует глубже изучать компиляторы и формальные грамматики.