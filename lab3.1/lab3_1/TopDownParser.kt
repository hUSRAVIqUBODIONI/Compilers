package com.example.lab3_1

import java.util.Stack

fun topDownParser(
    tokens: List<Token>,
    table: Map<String, List<Map<String, List<String>>>>,
    start: String
) {
    val stack = Stack<String>()
    stack.push(start)

    var index = 0
    val inputTokens = tokens.toMutableList()
    inputTokens.add(Token("$", "$"))
    while (stack.isNotEmpty()) {
        val top = stack.peek()
        val currentToken = inputTokens[index]

        if (top == currentToken.type || top == currentToken.value) {
            stack.pop()
            index++
            continue
        }

        val rulesForNonTerminal = table[top]
        if (rulesForNonTerminal == null) {
            println("Синтаксическая ошибка: Нет правил для нетерминала $top")
            kotlin.system.exitProcess(1)
        }

        var production: List<String>? = null
        for (ruleSet in rulesForNonTerminal) {
            if (ruleSet.containsKey(currentToken.type)) {
                production = ruleSet[currentToken.type]
                break
            }
        }

        if (production == null) {
            val expectedTokens = rulesForNonTerminal.flatMap { it.keys }.distinct()
            println("Синтаксическая ошибка:$top Неожиданный токен ${currentToken.value} (тип: ${currentToken.type}). Ожидалось одно из: $expectedTokens")
            kotlin.system.exitProcess(1)

        }
        stack.pop()
        for (symbol in production.reversed()) {
            if (symbol != "eps") {
                stack.push(symbol)
            }
        }
    }
    if (index != inputTokens.size - 1) {
        println(
            "Синтаксическая ошибка: Не все токены обработаны. Осталось: ${
                inputTokens.drop(
                    index
                ).joinToString(" ") { it.value }
            }"
        )
        kotlin.system.exitProcess(1)
    }

    println("Парсинг успешно завершен!")
}