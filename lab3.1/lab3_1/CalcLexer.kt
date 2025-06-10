package com.example.lab3_1

import java.io.File

class Token(val type: String, val value: String) {
    override fun toString(): String = "Token(type='$type', value='$value')"
}

class Lexer(private val fileName: String) {
    private val lines: List<String> = File(fileName).readLines()

    fun parse(): List<Token> {
        val tokens = mutableListOf<Token>()

        val patterns = listOf(
            "left_paren" to Regex("^\\("),
            "right_paren" to Regex("^\\)"),
            "plus_sign" to Regex("^\\+"),
            "minus" to Regex("^\\-"),
            "star" to Regex("^\\*"),
            "slash" to Regex("^\\/"),
            "n" to Regex("^[0-9]+")
        )

        lines.forEach { line ->
            var currentLine = line.trim()
            while (currentLine.isNotEmpty()) {
                if (currentLine[0].isWhitespace()) {
                    currentLine = currentLine.substring(1)
                    continue
                }

                var matched = false
                for ((type, regex) in patterns) {
                    val match = regex.find(currentLine)
                    if (match != null) {
                        val value = match.value
                        tokens.add(Token(type, value))
                        currentLine = currentLine.substring(value.length)
                        matched = true
                        break
                    }
                }

                if (!matched) {
                    // Пропускаем нераспознанный символ
                    currentLine = currentLine.substring(1)
                }
            }
        }

        return tokens
    }
}