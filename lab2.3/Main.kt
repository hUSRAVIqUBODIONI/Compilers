package lab2_3 
import java.io.File
import java.io.InputStream
import lab2_3.Tokenize
fun main() {
    val inputStream: InputStream = File("/Users/husravi_qubodioni/Desktop/Git-reps/Compilers/lab2.3/example.txt").inputStream()
    val inputString = inputStream.bufferedReader().use { it.readText() }
    val Tokenizer = Tokenize(inputString)
    Tokenizer.tokenize().forEach {
        print("${it.type} ")
    }
    val parser = Parser(Tokenizer.tokens)
    parser.parse()
}