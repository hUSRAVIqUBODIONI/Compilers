package lab2_3
import lab2_3.Tokenize
import lab2_3.Parser
import lab2_3.generateDotString

import java.io.File

fun main() {

    val inputPath = "/Users/husravi_qubodioni/Desktop/Git-reps/Compilers/lab2.3/example.txt"
    val inputText = File(inputPath).readText()
    val tokenizer = Tokenize(inputText)
    val tokens = tokenizer.tokenize()
    tokens.forEach{
        println(it)
    }
    val parser = Parser(tokens.toMutableList())
    val tree = parser.parse()
    val dotOutput = generateDotString(tree)
    File("/Users/husravi_qubodioni/Desktop/Git-reps/Compilers/lab2.3/parse_tree.dot").writeText(dotOutput)
}


// dot -Tpng parse_tree.dot -o tree.png