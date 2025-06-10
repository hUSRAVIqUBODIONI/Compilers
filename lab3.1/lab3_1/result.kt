package com.example.lab.lab3_1



val Start = "S"

val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(
    "S" to listOf(
        mapOf("n" to listOf("T", "E1"),
"left_paren" to listOf("T", "E1"),
    )),
    "E1" to listOf(
        mapOf("plus_sign" to listOf("plus_sign", "T", "E1"),
"right_paren" to listOf("eps"),
"$" to listOf("eps"),
    )),
    "T" to listOf(
        mapOf("n" to listOf("F", "T1"),
"left_paren" to listOf("F", "T1"),
    )),
    "T1" to listOf(
        mapOf("plus_sign" to listOf("eps"),
"star" to listOf("B", "F", "T1"),
"right_paren" to listOf("eps"),
"slash" to listOf("B", "F", "T1"),
"$" to listOf("eps"),
    )),
    "B" to listOf(
        mapOf("star" to listOf("star"),
"slash" to listOf("slash"),
    )),
    "F" to listOf(
        mapOf("n" to listOf("n"),
"left_paren" to listOf("left_paren", "S", "right_paren"),
    )),
)
