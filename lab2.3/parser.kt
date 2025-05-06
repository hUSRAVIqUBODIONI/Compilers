package com.example.lab

class Parser(val tokens: MutableList<Token>) {
    private val tokenIterator = tokens.iterator() // Итератор по токенам
    private val parseStack = mutableListOf<String>() // Стек для хранения правил

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

    // Парсинг таблицы
    val parseTable = mapOf<String, List<Map<String, List<String>>>>(
        GRAMMAR to listOf(
            mapOf(KEY_TOKENS to listOf(TOKENS, RULES, START))
        ),
        START to listOf(
            mapOf(KEY_START to listOf(KEY_START, NAME,DOT))
        ),
        TOKENS to listOf(
            mapOf(KEY_TOKENS to listOf(TOKEN, TOKENS), NAME to listOf(EPS))
        ),
        TOKEN to listOf(
            mapOf(KEY_TOKENS to listOf(KEY_TOKENS, NAME, TOKEN_LIST, DOT))
        ),
        TOKEN_LIST to listOf(
            mapOf(COMMA to listOf(COMMA, NAME, TOKEN_LIST),DOT to listOf(EPS))
        ),
        RULES to listOf(
            mapOf(NAME to listOf(UNIT, UNITS))
        ),
        UNIT to listOf(
            mapOf(NAME to listOf(NAME, IS, RULE_LIST, END))
        ),
        RULE_LIST to listOf(
            mapOf(NAME to listOf(NAME, RULE_LIST), COMMA to listOf(EPS),DOT to listOf(EPS))
        ),
        END to listOf(
            mapOf(COMMA to listOf(COMMA), DOT to listOf(DOT))
        ),
        UNITS to listOf(
            mapOf(NAME to listOf(UNIT, UNITS), KEY_START to listOf(EPS))
        )
    )

    fun parse() {
        val parseStack: ArrayDeque<String> = ArrayDeque()
        var token = tokenIterator.nextOrNull()
        parseStack.addFirst(GRAMMAR)

        while (parseStack.isNotEmpty()) {
            val currentRule = parseStack.removeFirst()

            if (currentRule == EPS) {
                continue
            }

            if (token == null) {
                throw IllegalArgumentException("❌ Ошибка синтаксиса: достигнут конец входных данных, ожидался '$currentRule'.")
            }

            if (isTerminal(currentRule)) {
                if ((currentRule == NAME && token.type == TokenType.VALUES) || currentRule == token.value) {

                    token = tokenIterator.nextOrNull()
                    if (token != null)
                    continue
                } else {
                    throw IllegalArgumentException("❌ Ошибка синтаксиса: ожидался '$currentRule', но найден '${token.value}' (${token.type}) на ${token.line}:${token.column}.")
                }
            } else {
                val productionRules = parseTable[currentRule]
                if (productionRules == null) {
                    throw IllegalArgumentException("❌ Ошибка: нет определений для нетерминала '$currentRule'.")
                }

                // Пытаемся найти подходящее правило по текущему токену

                val selectedRule = if(token.type != TokenType.VALUES){productionRules[0].get(token.value)}
                else{productionRules[0].get(NAME)}

                if (selectedRule != null) {


                    for (symbol in selectedRule.reversed()) {

                        parseStack.addFirst(symbol)

                    }

                } else {
                    throw IllegalArgumentException("❌ Ошибка: не найдено правил для '$currentRule' при токене '${token.value}' (${token.type}).")
                }
            }
        }
        println("✅ Разбор завершён успешно!")
    }



    // Функция для проверки, является ли правило терминалом
    fun isTerminal(rule: String): Boolean {

        return rule[0].isLowerCase() || rule[0] ==',' || rule[0] == '.'
    }

    // Расширение для получения следующего токена или null, если их больше нет
    fun <T> Iterator<T>.nextOrNull(): T? {
        return if (hasNext()) next() else null
    }
}