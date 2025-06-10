package com.example.lab.lab2_3

import com.example.lab.SemanticAnalyzer
import com.example.lab3_1.TableGenerator
import java.io.File

fun main() {

    val inputPath = "/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab/lab2_3/example.txt"
    val inputText = File(inputPath).readText()
    val tokenizer = Tokenize(inputText)
    val tokens = tokenizer.tokenize()

    val parser = Parser(tokens)
    val ast = parser.parse()
    val dotGenerator = DotGenerator()
    val dotString = dotGenerator.generateDotString(ast)
    File("/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab/lab2_3/parse_tree.dot").writeText(dotString)

    val semanticAnalyzer = SemanticAnalyzer(ast.children[0])
    semanticAnalyzer.parseGrammarNode()

    val grammarPath = "/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab3_1/grammar_new.txt"
    val grammarText = File(grammarPath).readText()
    val table = TableGenerator(grammarText).parseGrammar().generateFirst().generateFollow().generateTable()
    table.printLL1Table("/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab/lab2_3/result.kt",
        "package com.example.lab.lab2_3")


    

    val CalcPath = "/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab3_1/calc_grammar.txt"
    val CaclText = File(CalcPath).readText()
    val Calctable = TableGenerator(CaclText).parseGrammar().generateFirst().generateFollow().generateTable()
    Calctable.printLL1Table("/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab3_1/result.kt",
        "package com.example.lab.lab3_1\n")


}


// dot -Tpng parse_tree.dot -o tree.png

