package com.example.lab

import java.io.File

fun main() {

    val inputPath = "/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab/example.txt"
    val inputText = File(inputPath).readText()
    val tokenizer = Tokenize(inputText)
    val tokens = tokenizer.tokenize()
    val parser = Parser(tokens)
    val tree = parser.parse()
    val dotOutput = generateDotString(tree)
    File("/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab/parse_tree.dot").writeText(dotOutput)
}


// dot -Tpng parse_tree.dot -o tree.png