package lab2_3 



enum class TokenType{
    TOKEN,VALUES,IS,DOT,COMMA,N,START,WHITESPACE
}

class Token(
    val type: TokenType,
    val value: String,
    val line: Int,
    val column: Int

)

class Tokenize(val text:String){
    val pattern = mapOf<TokenType, Regex>(
        TokenType.TOKEN to Regex("\\b(tokens)\\b"),
        TokenType.VALUES to Regex("\\(.+?\\)"),
        TokenType.DOT to Regex("\\."),
        TokenType.IS to Regex("\\b(is)\\b"),
        TokenType.COMMA to Regex(","),
        TokenType.START to Regex("\\b(start)\\b"),
        TokenType.WHITESPACE to Regex("\\s+")
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

                    // Добавляем токен
                    if (type != TokenType.WHITESPACE)
                    {
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