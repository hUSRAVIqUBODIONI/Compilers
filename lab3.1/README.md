% Лабораторная работа № 3.1 «Самоприменимый генератор компиляторов
  на основе предсказывающего анализа»
% 21 мая 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является изучение алгоритма построения таблиц предсказывающего анализатора.
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
# Грамматика на входном языке

```
tokens (is), (tokens), (comma), (dot), (left paren), (right paren), (name), (start).
(GRAMMAR)   is (TOKENS) (RULES) (START).
(TOKENS)    is (TOKEN) (TOKENS),
(TOKENS)    is .
(TOKEN) is (tokens) (name) (TOKENLIST) (dot).
(TOKENLIST) is (comma) (name) (TOKENLIST),
(TOKENLIST) is .
(RULES)     is (UNIT) (UNITS).
(UNIT)      is (name) (is) (RULELIST) (END).
(RULELIST) is (name) (RULELIST),
(RULELIST) is .
(END) is (comma),
(END) is (dot).
(UNITS)      is (UNIT) (UNITS),
(UNITS)      is .
(START)     is (start) (name)  (dot).
start (GRAMMAR).
```

# Реализация
## Генератор компиляторов

```
fun generateFirst(): TableGenerator {
        terminals.forEach {
            First[it] = mutableSetOf(it)
        }

        nonTerminals.forEach {
            First[it] = mutableSetOf<String>()
        }

        First["eps"] = mutableSetOf("eps")

        var changed = true
        while (changed) {
            changed = false

            productions.forEach { (nonTerminal, rules) ->
                rules.forEach { rule ->
                    val oldFirst = First[nonTerminal]!!.toSet()
                    var allEpsilon = true

                    for (symbol in rule) {
                        if (symbol in terminals || symbol == "eps") {
                            if (symbol != "eps") {
                                First[nonTerminal]!!.add(symbol)
                            }
                            allEpsilon = symbol == "eps"
                            break
                        } else {
                            First[nonTerminal]!!.addAll(First[symbol]!!.minus("eps"))
                            if ("eps" !in First[symbol]!!) {
                                allEpsilon = false
                                break
                            }
                        }
                    }

                    if (allEpsilon) {
                        First[nonTerminal]!!.add("eps")
                    }

                    if (First[nonTerminal]!! != oldFirst) {
                        changed = true
                    }
                }
            }
        }

        return this
    }


    fun generateFollow(): TableGenerator {
        nonTerminals.forEach {
            Follow[it] = mutableSetOf()
        }

        val startSymbol = productions.first().left
        Follow[startSymbol]!!.add("$")

        var changed = true
        while (changed) {
            changed = false

            for ((lhs, rules) in productions) {
                for (rule in rules) {
                    for ((index, symbol) in rule.withIndex()) {
                        if (symbol in nonTerminals) {
                            val followBefore = Follow[symbol]!!.toSet()

                            val nextSymbols = rule.drop(index + 1)

                            if (nextSymbols.isNotEmpty()) {
                                val firstOfNext = computeFirstOfSequence(nextSymbols)
                                Follow[symbol]!!.addAll(firstOfNext - "eps")

                                if ("eps" in firstOfNext) {
                                    Follow[symbol]!!.addAll(Follow[lhs]!!)
                                }
                            } else {
                                Follow[symbol]!!.addAll(Follow[lhs]!!)
                            }

                            if (Follow[symbol]!!.size > followBefore.size) {
                                changed = true
                            }
                        }
                    }
                }
            }
        }
        return this
    }


    private fun computeFirstOfSequence(symbols: List<String>): Set<String> {
        val result = mutableSetOf<String>()
        for (symbol in symbols) {
            val firstSet = First[symbol] ?: emptySet()
            result.addAll(firstSet - "eps")

            if ("eps" !in firstSet) {
                return result
            }
        }
        result.add("eps")
        return result
    }


    fun generateTable(): TableGenerator {
        createEmptyTable()

        productions.forEach { production ->
            val nonTerminal = production.left
            production.right.forEach { rule ->
                if (rule == listOf("eps")) {
                    Follow[nonTerminal]?.forEach { terminal ->
                        table[nonTerminal]?.get(terminal)?.add("eps")
                    }
                } else {
                    var canDeriveEps = true
                    for (symbol in rule) {
                        if (symbol in terminals) {
                            if (symbol != "eps") {
                                table[nonTerminal]?.get(symbol)?.add(rule.joinToString(" "))
                                canDeriveEps = false
                                break
                            }
                        } else if (symbol in nonTerminals) {
                            First[symbol]?.forEach { firstSymbol ->
                                if (firstSymbol != "eps") {
                                    table[nonTerminal]?.get(firstSymbol)?.add(rule.joinToString(" "))
                                }
                            }

                            if ("eps" !in First[symbol]!!) {
                                canDeriveEps = false
                                break
                            }
                        }
                    }
                    if (canDeriveEps) {
                        Follow[nonTerminal]?.forEach { terminal ->
                            table[nonTerminal]?.get(terminal)?.add(rule.joinToString(" "))
                        }
                    }
                }
            }
        }

        return this
    }

    private fun createEmptyTable() {
        nonTerminals.forEach { nonTerminal ->
            table[nonTerminal] = mutableMapOf()

            terminals.forEach { terminal ->
                table[nonTerminal]!![terminal] = mutableListOf()
            }
            table[nonTerminal]!!["$"] = mutableListOf()
        }
    }


    fun printLL1Table(filePath: String,pack: String) {

        val parseTable = table.map { (nonTerminal, terminalMap) ->
            nonTerminal to terminalMap.mapNotNull { (terminal, rules) ->
                if (rules.isNotEmpty()) {
                    terminal to rules
                } else {
                    null
                }
            }.toMap()
        }.toMap()


        val file = File(filePath)
        file.printWriter().use { writer ->
            writer.println("$pack\n")
            writer.println()
            writer.println("val Start = \"$start\"\n")
            writer.println("val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(")


            parseTable.forEach { (nonTerminal, terminalMap) ->
                writer.print("    \"$nonTerminal\" to listOf(")

                writer.println()
                writer.print("        mapOf(")
                terminalMap.forEach { (terminal, rules) ->
                    writer.print("\"$terminal\" to listOf(")
                    val list_rules = rules[0].split(" ")
                    writer.print(list_rules.joinToString(", ") { "\"$it\"" })
                    writer.println("),")
                }

                writer.println("    )),")
            }

            writer.println(")")
        }
    }
```

## Калькулятор

```
package com.example.lab3_1

sealed class Node {
    data class Number(val value: String) : Node()
    data class Operator(val value: String, val left: Node, val right: Node) : Node()
}

val precedence = mapOf(
    "plus_sign" to 1,
    "minus_sign" to 1,
    "star" to 2,
    "slash" to 2
)

fun parseExpression(tokens: List<Token>): Node {
    fun getPrecedence(type: String): Int = precedence[type] ?: -1

    fun isOperator(token: Token) = precedence.containsKey(token.type)

    fun parse(tokens: List<Token>, minPrecedence: Int = 0): Pair<Node, Int> {
        fun parsePrimary(index: Int): Pair<Node, Int> {
            val token = tokens[index]
            return when (token.type) {
                "n" -> Node.Number(token.value) to index + 1
                "left_paren" -> {
                    val (node, nextIndex) = parse(tokens.subList(index + 1, tokens.size))
                    if (tokens[index + 1 + nextIndex].type != "right_paren") {
                        throw IllegalArgumentException("Expected right parenthesis")
                    }
                    node to index + 2 + nextIndex
                }
                else -> throw IllegalArgumentException("Unexpected token: $token")
            }
        }

        var (lhs, index) = parsePrimary(0)

        while (index < tokens.size) {
            val token = tokens[index]
            if (!isOperator(token)) break

            val prec = getPrecedence(token.type)
            if (prec < minPrecedence) break

            val opToken = token
            index += 1

            val (rhs, nextIndex) = parse(tokens.subList(index, tokens.size), prec + 1)
            lhs = Node.Operator(opToken.value, lhs, rhs)
            index += nextIndex
        }

        return lhs to index
    }

    return parse(tokens).first
}

fun printTree(node: Node, indent: String = "") {
    when (node) {
        is Node.Number -> println("$indent${node.value}")
        is Node.Operator -> {
            println("$indent${node.value}")
            printTree(node.left, indent + "  ")
            printTree(node.right, indent + "  ")
        }
    }
}

fun evaluate(node: Node): Double {
    return when (node) {
        is Node.Number -> node.value.toDouble()
        is Node.Operator -> {
            val leftValue = evaluate(node.left)
            val rightValue = evaluate(node.right)
            when (node.value) {
                "+" -> leftValue + rightValue
                "-" -> leftValue - rightValue
                "*" -> leftValue * rightValue
                "/" -> leftValue / rightValue
                else -> throw IllegalArgumentException("Unknown operator: ${node.value}")
            }
        }
    }
}
```

# Тестирование
## Генератор компиляторов

Таблица для калькулятора

```
package com.example.lab.lab3_1
val Start = "S"

val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(
    "S" to listOf(
        mapOf("n" to listOf("T", "E1"),
"left_paren" to listOf("T", "E1"),
    )),
    "E1" to listOf(
        mapOf("plus_sign" to listOf("plus_sign", "T", "E1"),
"right_paren" to listOf("eps"),
"$" to listOf("eps"),
    )),
    "T" to listOf(
        mapOf("n" to listOf("F", "T1"),
"left_paren" to listOf("F", "T1"),
    )),
    "T1" to listOf(
        mapOf("plus_sign" to listOf("eps"),
"star" to listOf("B", "F", "T1"),
"right_paren" to listOf("eps"),
"slash" to listOf("B", "F", "T1"),
"$" to listOf("eps"),
    )),
    "B" to listOf(
        mapOf("star" to listOf("star"),
"slash" to listOf("slash"),
    )),
    "F" to listOf(
        mapOf("n" to listOf("n"),
"left_paren" to listOf("left_paren", "S", "right_paren"),
    )),
)
```

Таблица для собственной грамматики

```
package com.example.lab.lab2_3
val Start = "GRAMMAR"

val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(
    "GRAMMAR" to listOf(
        mapOf("tokens" to listOf("TOKENS", "RULES", "START"),
"name" to listOf("TOKENS", "RULES", "START"),
    )),
    "TOKENS" to listOf(
        mapOf("tokens" to listOf("TOKEN", "TOKENS"),
"name" to listOf("eps"),
    )),
    "TOKEN" to listOf(
        mapOf("tokens" to listOf("tokens", "name", "TOKENLIST", "dot"),
    )),
    "TOKENLIST" to listOf(
        mapOf("comma" to listOf("comma", "name", "TOKENLIST"),
"dot" to listOf("eps"),
    )),
    "RULES" to listOf(
        mapOf("name" to listOf("UNIT", "UNITS"),
    )),
    "UNIT" to listOf(
        mapOf("name" to listOf("name", "is", "RULELIST", "END"),
    )),
    "RULELIST" to listOf(
        mapOf("comma" to listOf("eps"),
"dot" to listOf("eps"),
"name" to listOf("name", "RULELIST"),
    )),
    "END" to listOf(
        mapOf("comma" to listOf("comma"),
"dot" to listOf("dot"),
    )),
    "UNITS" to listOf(
        mapOf("name" to listOf("UNIT", "UNITS"),
"start" to listOf("eps"),
    )),
    "START" to listOf(
        mapOf("start" to listOf("start", "name", "dot"),
    )),
)

```

## Калькулятор
Сначала входное выражение разбивается на токены - числа, операторы и скобки. Затем парсер анализирует 
последовательность токенов, используя заранее сгенерированную таблицу предсказаний. В процессе разбора 
постепенно строится абстрактное синтаксическое дерево. Проходя по дереву получаем ответ.

# Вывод
Эта лабораторная работа, на мой взгляд, оказалась самой сложной за весь курс. Причем сложность заключалась
не в написании кода (умные люди уже давно придумали псевдо-код для генерации FIRST, FOLLOW и таблицы
предсказаний), а именно в реализации. Большую часть времени я потратил на то, чтобы разобраться в самой
сути задания, но теперь, глядя на результат, понимаю, что оно того стоило.

Теперь, если мне когда-нибудь понадобится построить предсказывающую таблицу для произвольной 
LL(1)-грамматики,я смогу смело использовать наработки из этой лабораторной, а не искать сторонние 
веб-ресурсы. Для большего удобства можно было бы добавить автоматическое устранение левой рекурсии 
и правого ветвления — это позволило бы приводить грамматику к LL(1)-виду (хотя и не во всех случаях). 
К счастью, эти алгоритмы уже были реализованы в рамках курса ТФЯ, так что при необходимости их можно 
легко интегрировать.

Если коротко: было больно но мне понравилось.