# Лабораторная работа по генерации лексического анализатора с использованием Flex

## 1. Цель работы
Изучение принципов работы генератора лексических анализаторов Flex и приобретение практических навыков создания лексических анализаторов для обработки входных данных согласно заданной спецификации.

## 2. Индивидуальный вариант

### 2.1 Поддерживаемые лексемы
1. **Числа**:
   - Десятичные цифры (0-9)
   - Могут начинаться с нуля

2. **Операторы**:
   - Арифметические: +, -, *, /
   - Скобки: (, )

3. **Комментарии**:
   - Обрамляются (* и *)
   - Не поддерживают вложенность

4. **Строки**:
   - Ограничены { и }
   - Escape-последовательности:
     - #{ → {
     - #} → }
     - /## → /#
     - #hh → символ с hex-кодом hh

### 2.2 Особые требования
- Строки не могут содержать неэкранированные переносы строк
- При обнаружении ошибок анализ должен продолжаться
- Обязательное ведение списка ошибок с координатами

## Тестирование 

### Входные данные 
```
(* heeey  dfd  big *)   +-*/    a
1234 shodi 

! # 

{ ## HELLO #{  heeere  #}  #FF (* jdkbnfksdnfng kflkdf kfjgl)
```

### Вывод на stdout
```
TOKENS (7):
(1,25)-(1,26) PLUS
(1,26)-(1,27) MINUS
(1,27)-(1,28) MULTIPLY
(1,28)-(1,29) DIVIDE
(1,33)-(1,34) IDENT a
(2,1)-(2,5) NUMBER 1234
(2,6)-(2,11) IDENT shodi

COMMENTS (1):
(1,1)-(1,22)

ERRORS (3):
Error (4,1): Invalid character
Error (4,3): Invalid character
Error (6,1): Unclosed string, expected '}'
```