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
