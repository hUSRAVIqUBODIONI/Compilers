package com.example.lab

import com.example.lab.lab3_1.GeneratedParseTable
import com.example.lab.lab3_1.Start
import com.example.lab3_1.Lexer
import com.example.lab3_1.TableGenerator
import com.example.lab3_1.evaluate
import com.example.lab3_1.parseExpression
import com.example.lab3_1.printTree
import com.example.lab3_1.topDownParser
import java.io.File


fun main(){
    val lexer = Lexer("/Users/husravi_qubodioni/AndroidStudioProjects/app/src/main/java/com/example/lab3_1/calc_text.txt").parse()
    println(lexer)
    topDownParser(lexer,GeneratedParseTable,Start)
    val tree = parseExpression(lexer)
    printTree(tree)
    val result = evaluate(tree)
    println("Result: $result")
}