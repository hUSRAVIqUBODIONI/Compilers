% Лабораторная работа № 2.3 «Синтаксический анализатор на основе
  предсказывающего анализа»
% 7 мая 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является изучение алгоритма построения таблиц предсказывающего 
анализатора.

# Индивидуальный вариант
```
tokens (plus sign), (star), (n).
tokens (left paren), (right paren).
(E)   is (T) (E 1).
(E 1) is (plus sign) (T) (E 1),
(E 1) is .
(T)   is (F) (T 1).
(T 1) is (star) (F) (T 1),
(T 1) is .
(F)   is (n),
(F)   is (left paren) (E) (right paren).
(* аксиома *)
start (E).
```
# Реализация

## Неформальное описание синтаксиса входного языка
Язык формально состоит из 3 частей. Первая часть где мы определяем токены (терминалы). 
Вторая часть, это часть правил. Если у правила нетерминала есть алтернава то каждое правило 
описывыем в отдельную строчку. Третья часть, обозночаем стартовый нетерминалФормально язык 
состоит из трёх частей. В первой части определяются токены. Во второй части записываются 
правила, каждое альтернативное правило для нетерминала пишется с новой строки. 
В третьей части указывается стартовый нетерминал.

## Лексическая структура
```
TokenType.TOKEN to Regex("\\b(tokens)\\b"),
TokenType.VALUES to Regex("\\(.+?\\)"),
TokenType.DOT to Regex("\\."),
TokenType.IS to Regex("\\b(is)\\b"),
TokenType.COMMA to Regex(","),
TokenType.START to Regex("\\b(start)\\b"),
TokenType.WHITESPACE to Regex("\\s+")
```
## Грамматика языка
```
GRAMMAR -> TOKENS UNIT UNITS AXIOM .
TOKENS -> tokens TOKENS_LIST DOT .
TOKENS_LIST -> NAME TOKENS_LIST | eps .
UNIT -> RULE RULES .
UNITS -> UNIT UNITS | eps .
AXIOM -> start NAME DOT .
RULE -> NAME is NAMES DOT .
RULES -> RULE RULES | eps .
NAMES -> NAME NAMES | eps .
```

## Программная реализация

```
package lab2_3

class Parser(val tokens: MutableList<Token>) {
    private val tokenIterator = tokens.iterator()

    val GRAMMAR = "GRAMMAR"
    val START = "START"
    val TOKENS = "TOKENS"
    val TOKEN = "TOKEN"
    val TOKEN_LIST = "TOKENLIST"
    val ALPHA = "ALPHA"
    val RULES = "RULES"
    val UNIT = "UNIT"
    val UNITS = "UNITS"
    val RULE_LIST = "RULELIST"
    val END = "END"
    val NAME = "name"
    val DOT = "."
    val COMMA = ","
    val IS = "is"
    val KEY_START = "start"
    val KEY_TOKENS = "tokens"
    val EPS = "eps"

    val parseTable = mapOf<String, List<Map<String, List<String>>>>(
        GRAMMAR to listOf(mapOf(KEY_TOKENS to listOf(TOKENS, RULES, START))),
        START to listOf(mapOf(KEY_START to listOf(KEY_START, NAME))),
        TOKENS to listOf(mapOf(KEY_TOKENS to listOf(TOKEN, TOKENS), NAME to listOf(EPS))),
        TOKEN to listOf(mapOf(KEY_TOKENS to listOf(KEY_TOKENS, NAME, TOKEN_LIST, DOT))),
        TOKEN_LIST to listOf(mapOf(COMMA to listOf(COMMA, NAME, ALPHA), DOT to listOf(EPS))),
        ALPHA to listOf(mapOf(COMMA to listOf(TOKEN_LIST), DOT to listOf(EPS))),
        RULES to listOf(mapOf(NAME to listOf(UNIT, UNITS))),
        UNIT to listOf(mapOf(NAME to listOf(NAME, IS, RULE_LIST, END))),
        RULE_LIST to listOf(mapOf(NAME to listOf(NAME, RULE_LIST), DOT to listOf(EPS), COMMA 
to listOf(EPS))),
        END to listOf(mapOf(COMMA to listOf(COMMA), DOT to listOf(DOT))),
        UNITS to listOf(mapOf(NAME to listOf(UNIT, UNITS), DOT to listOf(EPS),KEY_START to 
listOf(EPS)))
    )

    fun parse(): ParseTreeNode {
        val parseStack: ArrayDeque<Pair<String, ParseTreeNode>> = ArrayDeque()
        val root = ParseTreeNode(GRAMMAR)
        parseStack.addFirst(GRAMMAR to root)
        var token = tokenIterator.nextOrNull()

        while (parseStack.isNotEmpty()) {
            val (currentRule, parentNode) = parseStack.removeFirst()

            if (currentRule == EPS) {
                parentNode.children.add(ParseTreeNode(EPS))
                continue
            }

            if (token == null) {
                throw IllegalArgumentException("Конец ввода. Ожидалось: '$currentRule'")
            }

            if (isTerminal(currentRule)) {
                if ((currentRule == NAME && token.type == TokenType.VALUES) || 
currentRule == token.value) {
                    parentNode.children.add(ParseTreeNode(token.value))
                    token = tokenIterator.nextOrNull()
                    continue
                } else {
                    throw IllegalArgumentException("Ожидалось: '$currentRule', найдено: 
'${token.value}' (${token.type}) на ${token.line}:${token.column}")
                }
            } else {
                val productionRules = parseTable[currentRule]
                    ?: throw IllegalArgumentException("Нет правил для '$currentRule'")

                val selectedRule = when {
                    token.type == TokenType.VALUES -> productionRules[0][NAME]
                    else -> productionRules[0][token.value]
                }

                if (selectedRule != null) {
                    val ruleNode = ParseTreeNode(currentRule)
                    parentNode.children.add(ruleNode)

                    for (symbol in selectedRule.reversed()) {
                        parseStack.addFirst(symbol to ruleNode)
                    }
                } else {
                    throw IllegalArgumentException("Нет правила для '$currentRule' 
при токене '${token.value}' (${token.type})")
                }
            }
        }

        println("Разбор завершён успешно.")
        return root
    }

    private fun isTerminal(rule: String): Boolean {
        return rule == NAME || rule == DOT || rule == COMMA 
|| rule == IS || rule == KEY_START || rule == KEY_TOKENS
    }

    private fun <T> Iterator<T>.nextOrNull(): T? = if (hasNext()) next() else null
}

```

# Тестирование

Входные данные

```
tokens (plus sign), (star), (n).
tokens (left paren), (right paren).
(E)   is (T) (E 1).
(E 1) is (plus sign) (T) (E 1),
(E 1) is .
(T)   is (F) (T 1).
(T 1) is (star) (F) (T 1),
(T 1) is .
(F)   is (n),
(F)   is (left paren) (E) (right paren).
start (E).
```

Вывод на `stdout`

```
digraph ParseTree {
node [shape=box];
node0 [label="GRAMMAR"];
node1 [label="GRAMMAR"];
node2 [label="TOKENS"];
node3 [label="TOKEN"];
node4 [label="tokens"];
node3 -> node4;
node5 [label="(plus sign)"];
node3 -> node5;
node6 [label="TOKENLIST"];
node7 [label=","];
node6 -> node7;
node8 [label="(star)"];
node6 -> node8;
node9 [label="ALPHA"];
node10 [label="TOKENLIST"];
node11 [label=","];
node10 -> node11;
node12 [label="(n)"];
node10 -> node12;
node13 [label="ALPHA"];
node14 [label="eps"];
node13 -> node14;
node10 -> node13;
node9 -> node10;
node6 -> node9;
node3 -> node6;
node15 [label="."];
node3 -> node15;
node2 -> node3;
node16 [label="TOKENS"];
node17 [label="TOKEN"];
node18 [label="tokens"];
node17 -> node18;
node19 [label="(left paren)"];
node17 -> node19;
node20 [label="TOKENLIST"];
node21 [label=","];
node20 -> node21;
node22 [label="(right paren)"];
node20 -> node22;
node23 [label="ALPHA"];
node24 [label="eps"];
node23 -> node24;
node20 -> node23;
node17 -> node20;
node25 [label="."];
node17 -> node25;
node16 -> node17;
node26 [label="TOKENS"];
node27 [label="eps"];
node26 -> node27;
node16 -> node26;
node2 -> node16;
node1 -> node2;
node28 [label="RULES"];
node29 [label="UNIT"];
node30 [label="(E)"];
node29 -> node30;
node31 [label="is"];
node29 -> node31;
node32 [label="RULELIST"];
node33 [label="(T)"];
node32 -> node33;
node34 [label="RULELIST"];
node35 [label="(E 1)"];
node34 -> node35;
node36 [label="RULELIST"];
node37 [label="eps"];
node36 -> node37;
node34 -> node36;
node32 -> node34;
node29 -> node32;
node38 [label="END"];
node39 [label="."];
node38 -> node39;
node29 -> node38;
node28 -> node29;
node40 [label="UNITS"];
node41 [label="UNIT"];
node42 [label="(E 1)"];
node41 -> node42;
node43 [label="is"];
node41 -> node43;
node44 [label="RULELIST"];
node45 [label="(plus sign)"];
node44 -> node45;
node46 [label="RULELIST"];
node47 [label="(T)"];
node46 -> node47;
node48 [label="RULELIST"];
node49 [label="(E 1)"];
node48 -> node49;
node50 [label="RULELIST"];
node51 [label="eps"];
node50 -> node51;
node48 -> node50;
node46 -> node48;
node44 -> node46;
node41 -> node44;
node52 [label="END"];
node53 [label=","];
node52 -> node53;
node41 -> node52;
node40 -> node41;
node54 [label="UNITS"];
node55 [label="UNIT"];
node56 [label="(E 1)"];
node55 -> node56;
node57 [label="is"];
node55 -> node57;
node58 [label="RULELIST"];
node59 [label="eps"];
node58 -> node59;
node55 -> node58;
node60 [label="END"];
node61 [label="."];
node60 -> node61;
node55 -> node60;
node54 -> node55;
node62 [label="UNITS"];
node63 [label="UNIT"];
node64 [label="(T)"];
node63 -> node64;
node65 [label="is"];
node63 -> node65;
node66 [label="RULELIST"];
node67 [label="(F)"];
node66 -> node67;
node68 [label="RULELIST"];
node69 [label="(T 1)"];
node68 -> node69;
node70 [label="RULELIST"];
node71 [label="eps"];
node70 -> node71;
node68 -> node70;
node66 -> node68;
node63 -> node66;
node72 [label="END"];
node73 [label="."];
node72 -> node73;
node63 -> node72;
node62 -> node63;
node74 [label="UNITS"];
node75 [label="UNIT"];
node76 [label="(T 1)"];
node75 -> node76;
node77 [label="is"];
node75 -> node77;
node78 [label="RULELIST"];
node79 [label="(star)"];
node78 -> node79;
node80 [label="RULELIST"];
node81 [label="(F)"];
node80 -> node81;
node82 [label="RULELIST"];
node83 [label="(T 1)"];
node82 -> node83;
node84 [label="RULELIST"];
node85 [label="eps"];
node84 -> node85;
node82 -> node84;
node80 -> node82;
node78 -> node80;
node75 -> node78;
node86 [label="END"];
node87 [label=","];
node86 -> node87;
node75 -> node86;
node74 -> node75;
node88 [label="UNITS"];
node89 [label="UNIT"];
node90 [label="(T 1)"];
node89 -> node90;
node91 [label="is"];
node89 -> node91;
node92 [label="RULELIST"];
node93 [label="eps"];
node92 -> node93;
node89 -> node92;
node94 [label="END"];
node95 [label="."];
node94 -> node95;
node89 -> node94;
node88 -> node89;
node96 [label="UNITS"];
node97 [label="UNIT"];
node98 [label="(F)"];
node97 -> node98;
node99 [label="is"];
node97 -> node99;
node100 [label="RULELIST"];
node101 [label="(n)"];
node100 -> node101;
node102 [label="RULELIST"];
node103 [label="eps"];
node102 -> node103;
node100 -> node102;
node97 -> node100;
node104 [label="END"];
node105 [label=","];
node104 -> node105;
node97 -> node104;
node96 -> node97;
node106 [label="UNITS"];
node107 [label="UNIT"];
node108 [label="(F)"];
node107 -> node108;
node109 [label="is"];
node107 -> node109;
node110 [label="RULELIST"];
node111 [label="(left paren)"];
node110 -> node111;
node112 [label="RULELIST"];
node113 [label="(E)"];
node112 -> node113;
node114 [label="RULELIST"];
node115 [label="(right paren)"];
node114 -> node115;
node116 [label="RULELIST"];
node117 [label="eps"];
node116 -> node117;
node114 -> node116;
node112 -> node114;
node110 -> node112;
node107 -> node110;
node118 [label="END"];
node119 [label="."];
node118 -> node119;
node107 -> node118;
node106 -> node107;
node120 [label="UNITS"];
node121 [label="eps"];
node120 -> node121;
node106 -> node120;
node96 -> node106;
node88 -> node96;
node74 -> node88;
node62 -> node74;
node54 -> node62;
node40 -> node54;
node28 -> node40;
node1 -> node28;
node122 [label="START"];
node123 [label="start"];
node122 -> node123;
node124 [label="(E)"];
node122 -> node124;
node1 -> node122;
node0 -> node1;
}
```

# Вывод
В этой работе я научился создавать предсказывающий анализатор с нуля. На самом деле, основы освоил
ещё на курсе ТФЯ, а эта лабораторная стала отличным повторением и закреплением материала.

Самой сложной частью оказалась разработка грамматики, которая корректно распознаёт заданный 
индивидуальный вариант. Основные трудности возникли при приведении её к LL(1)-виду, ведь предсказывающая 
таблица работает только для LL(1)-грамматик. 

Зато построение самой таблицы предсказаний и реализация парсера прошли довольно гладко. Для таблицы помогли 
онлайн-ресурсы с автоматизированными проверками, а за основу парсера взял код из лекций — получилось 
быстро и эффективно.

В целом, работа позволила глубже разобраться в теории формальных языков и на практике убедиться, 
как важно правильно составлять грамматику для корректного разбора.