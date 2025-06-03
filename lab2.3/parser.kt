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
        RULE_LIST to listOf(mapOf(NAME to listOf(NAME, RULE_LIST), DOT to listOf(EPS), COMMA to listOf(EPS))),
        END to listOf(mapOf(COMMA to listOf(COMMA), DOT to listOf(DOT))),
        UNITS to listOf(mapOf(NAME to listOf(UNIT, UNITS), DOT to listOf(EPS),KEY_START to listOf(EPS)))
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
                throw IllegalArgumentException("❌ Конец ввода. Ожидалось: '$currentRule'")
            }

            if (isTerminal(currentRule)) {
                if ((currentRule == NAME && token.type == TokenType.VALUES) || currentRule == token.value) {
                    parentNode.children.add(ParseTreeNode(token.value))
                    token = tokenIterator.nextOrNull()
                    continue
                } else {
                    throw IllegalArgumentException("❌ Ожидалось: '$currentRule', найдено: '${token.value}' (${token.type}) на ${token.line}:${token.column}")
                }
            } else {
                val productionRules = parseTable[currentRule]
                    ?: throw IllegalArgumentException("❌ Нет правил для '$currentRule'")

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
                    throw IllegalArgumentException("❌ Нет правила для '$currentRule' при токене '${token.value}' (${token.type})")
                }
            }
        }

        println("✅ Разбор завершён успешно.")
        return root
    }

    private fun isTerminal(rule: String): Boolean {
        return rule == NAME || rule == DOT || rule == COMMA || rule == IS || rule == KEY_START || rule == KEY_TOKENS
    }

    private fun <T> Iterator<T>.nextOrNull(): T? = if (hasNext()) next() else null
}
