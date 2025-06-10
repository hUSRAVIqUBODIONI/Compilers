package com.example.lab.lab2_3




class Parser(val tokens: List<Token>) {
    private val tokenIterator = tokens.iterator()

    val GRAMMAR = "GRAMMAR"
    val START = "START"
    val TOKENS = "TOKENS"
    val TOKEN = "TOKEN"
    val TOKENLIST = "TOKENLIST"
    val RULES = "RULES"
    val UNIT = "UNIT"
    val UNITS = "UNITS"
    val RULELIST = "RULELIST"
    val END = "END"
    val NAME = "name"
    val DOT = "dot"
    val COMMA = "comma"
    val IS = "is"
    val KEYSTART = "start"
    val KEYTOKENS = "tokens"
    val EPS = "eps"


    //val parseTable = GeneratedParseTable




    val parseTable = mapOf<String, List<Map<String, List<String>>>>(
        GRAMMAR to listOf(mapOf(KEYTOKENS to listOf(TOKENS, RULES, START))),
        START to listOf(mapOf(KEYSTART to listOf(KEYSTART, NAME))),
        TOKENS to listOf(mapOf(KEYTOKENS to listOf(TOKEN, TOKENS), NAME to listOf(EPS))),
        TOKEN to listOf(mapOf(KEYTOKENS to listOf(KEYTOKENS, NAME, TOKENLIST, DOT))),
        TOKENLIST to listOf(mapOf(COMMA to listOf(COMMA, NAME, TOKENLIST), DOT to listOf(EPS))),
        RULES to listOf(mapOf(NAME to listOf(UNIT, UNITS))),
        UNIT to listOf(mapOf(NAME to listOf(NAME, IS, RULELIST, END))),
        RULELIST to listOf(mapOf(NAME to listOf(NAME, RULELIST), DOT to listOf(EPS), COMMA to listOf(EPS))),
        END to listOf(mapOf(COMMA to listOf(COMMA), DOT to listOf(DOT))),
        UNITS to listOf(mapOf(NAME to listOf(UNIT, UNITS), DOT to listOf(EPS),KEYSTART to listOf(EPS)))
    )



    fun parse(): ASTNode {
        val parseStack: ArrayDeque<Pair<String, ASTNode>> = ArrayDeque()
        val root = ASTNode(GRAMMAR)
        parseStack.addFirst(GRAMMAR to root)
        var token = tokenIterator.nextOrNull()

        while (parseStack.isNotEmpty()) {
            val (currentSymbol, parentNode) = parseStack.removeFirst()

            if (currentSymbol == EPS) {
                parentNode.children.add(ASTNode(EPS))
                continue
            }

            if (token == null) {
                println("Конец ввода. Ожидалось: '$currentSymbol'")
                kotlin.system.exitProcess(1)
            }

            if (isTerminal(currentSymbol)) {
                if ((currentSymbol == NAME && token.type == "values") || currentSymbol == token.type) {
                    val newNode = ASTNode(currentSymbol, token = token)
                    parentNode.children.add(newNode)
                    token = tokenIterator.nextOrNull()
                    continue
                } else {
                    println("Ожидалось: '$currentSymbol', найдено: '${token.value}' (${token.type}) на ${token.line}:${token.column}")
                    kotlin.system.exitProcess(1)
                }
            } else {
                val productionRules = parseTable[currentSymbol]

                if (productionRules == null){
                        println("Нет правил для '$currentSymbol'")
                        kotlin.system.exitProcess(1)
                }

                val selectedRule = when {
                    token.type == "values" -> productionRules[0][NAME]
                    else -> productionRules[0][token.type]
                }

                if (selectedRule != null) {
                    val ruleNode = ASTNode(currentSymbol)
                    parentNode.children.add(ruleNode)

                    for (symbol in selectedRule.reversed()) {
                        parseStack.addFirst(symbol to ruleNode)
                    }
                } else {
                    println("Нет правила для '$currentSymbol' при токене '${token.value}' (${token.type})")
                    kotlin.system.exitProcess(1)
                }
            }
        }

        println("Разбор завершён успешно.")
        return root
    }


    private fun isTerminal(rule: String): Boolean {
        return rule == NAME || rule == DOT || rule == COMMA || rule == IS || rule == KEYSTART || rule == KEYTOKENS
    }

    private fun <T> Iterator<T>.nextOrNull(): T? = if (hasNext()) next() else null
}
