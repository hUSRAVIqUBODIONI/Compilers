package com.example.lab

import java.io.File
import java.io.InputStream

fun main() {
    val inputStream: InputStream = File("/Users/husravi_qubodioni/Desktop/Git-reps/Compilers/lab2.3/Lab/app/src/main/java/com/example/lab/example.txt").inputStream()
    val inputString = inputStream.bufferedReader().use { it.readText() }
    val Tokenizer = Tokenize(inputString)
    Tokenizer.tokenize().forEach {
        print("${it.type} ")
    }
}