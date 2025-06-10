package com.example.lab.lab2_3

import kotlin.collections.iterator

class Token(
    val type: String,  // Заменили enum на String
    val value: String,
    val line: Int,
    val column: Int
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Token) return false
        return this.value == other.value
    }

    override fun hashCode(): Int {
        return value.hashCode()
    }

    override fun toString(): String {
        return "TokenType: $type, Value: $value, at coord: $line,$column"
    }
}

class Tokenize(val text: String) {
    // Паттерны теперь используют строковые типы в нижнем регистре
    val pattern = mapOf(
        "comment" to Regex("\\(\\*.*\\*\\)"),
        "tokens" to Regex("\\b(tokens)\\b"),
        "values" to Regex("\\(.+?\\)"),
        "dot" to Regex("\\."),
        "is" to Regex("\\b(is)\\b"),
        "comma" to Regex(","),
        "start" to Regex("\\b(start)\\b"),
        "whitespace" to Regex("\\s+")
    )

    val tokens = mutableListOf<Token>()

    fun tokenize(): List<Token> {
        var currentIndex = 0
        var line = 1
        var column = 1

        while (currentIndex < text.length) {
            var matchFound = false

            for ((type, regex) in pattern) {
                val match = regex.find(text, currentIndex)
                if (match != null && match.range.first == currentIndex) {
                    val value = match.value

                    // Пропускаем пробелы и комментарии
                    if (type != "whitespace" && type != "comment") {
                        tokens.add(
                            Token(
                                type = type,
                                value = value,
                                line = line,
                                column = column
                            )
                        )
                    }

                    // Обновляем позицию
                    val lines = value.split("\n")
                    if (lines.size > 1) {
                        line += lines.size - 1
                        column = lines.last().length + 1
                    } else {
                        column += value.length
                    }

                    currentIndex += value.length
                    matchFound = true
                    break
                }
            }

            if (!matchFound) {
                throw IllegalArgumentException("Unexpected token at line $line, column $column: '${text[currentIndex]}'")
            }
        }
        return tokens
    }
}