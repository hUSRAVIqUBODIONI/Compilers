package com.example.lab.lab2_3


val Start = "GRAMMAR"

val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(
    "GRAMMAR" to listOf(
        mapOf("tokens" to listOf("TOKENS", "RULES", "START"),
"name" to listOf("TOKENS", "RULES", "START"),
    )),
    "TOKENS" to listOf(
        mapOf("tokens" to listOf("TOKEN", "TOKENS"),
"name" to listOf("eps"),
    )),
    "TOKEN" to listOf(
        mapOf("tokens" to listOf("tokens", "name", "TOKENLIST", "dot"),
    )),
    "TOKENLIST" to listOf(
        mapOf("comma" to listOf("comma", "name", "TOKENLIST"),
"dot" to listOf("eps"),
    )),
    "RULES" to listOf(
        mapOf("name" to listOf("UNIT", "UNITS"),
    )),
    "UNIT" to listOf(
        mapOf("name" to listOf("name", "is", "RULELIST", "END"),
    )),
    "RULELIST" to listOf(
        mapOf("comma" to listOf("eps"),
"dot" to listOf("eps"),
"name" to listOf("name", "RULELIST"),
    )),
    "END" to listOf(
        mapOf("comma" to listOf("comma"),
"dot" to listOf("dot"),
    )),
    "UNITS" to listOf(
        mapOf("name" to listOf("UNIT", "UNITS"),
"start" to listOf("eps"),
    )),
    "START" to listOf(
        mapOf("start" to listOf("start", "name", "dot"),
    )),
)
