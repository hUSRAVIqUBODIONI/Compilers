package com.example.lab3_1

import java.io.File

data class Production(val left: String, val right: MutableList<List<String>>)

class TableGenerator(val grammar: String) {

    var First: MutableMap<String, MutableSet<String>> = mutableMapOf()
    var Follow: MutableMap<String, MutableSet<String>> = mutableMapOf()
    val table: MutableMap<String, MutableMap<String, MutableList<String>>> = mutableMapOf()
    val terminals = mutableListOf<String>()
    val nonTerminals = mutableSetOf<String>()
    var start = ""
    lateinit var productions: MutableList<Production>

    fun parseGrammar(): TableGenerator {
        val lines = grammar.trim().lines().map { it.trim() }.filter { it.isNotEmpty() }
        productions = mutableListOf()
        nonTerminals.clear()
        terminals.clear()


        lines.find { it.startsWith("tokens") }?.let { tokensLine ->
            tokensLine.removePrefix("tokens")
                .split("""\s*,\s*|\s*\.\s*""".toRegex())
                .map {
                    it.trim().removeSurrounding("(", ")")
                }
                .filter { it.isNotEmpty() }
                .forEach {
                    terminals.add(it)
                }
        }


        for (line in lines) {
            when {
                line.startsWith("tokens") -> continue
                line.startsWith("start") -> {
                    start = line.removeSurrounding("start ", ".")
                        .trim().removeSurrounding("(", ")")
                }
                else -> parseProductionLine(line)
            }
        }
        val firstDuplicate = terminals
            .groupBy { it }
            .filter { it.value.size > 1 }
            .keys
            .firstOrNull()
        if (firstDuplicate != null){
            println("терминал (токен) объявлен дважды: $firstDuplicate")
            kotlin.system.exitProcess(1)
        }

        return this
    }

    private fun parseProductionLine(line: String) {
        if (!line.contains("is")) return

        val (leftPart, rightPart) = line.split("is", limit = 2)
        val left = leftPart.trim().removeSurrounding("(", ")")
        nonTerminals.add(left)

        val alternatives = mutableListOf<List<String>>()


        val cleanRight = rightPart.replace("),", ") ,")
            .replace(").", ") .")



        cleanRight.split("""\s*\.\s*""".toRegex()).first()
            .split("""\s*,\s*""".toRegex())
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .forEach { alternative ->

                    val symbols = alternative.split("\\s+".toRegex())
                        .map { it.removeSurrounding("(", ")") }
                        .filter { it.isNotEmpty() }
                    if (symbols.isNotEmpty()) {
                        alternatives.add(symbols)

                }
            }


        if (rightPart.trim().endsWith(".") && alternatives.isEmpty()) {
            alternatives.add(listOf("eps"))
        }

        if (alternatives.isNotEmpty()) {
            val production = productions.find { it.left == left }
            if (production != null) production.right.add(alternatives[0])
            else productions.add(Production(left=left,right = alternatives))
        }
    }


    fun generateFirst(): TableGenerator {
        terminals.forEach {
            First[it] = mutableSetOf(it)
        }

        nonTerminals.forEach {
            First[it] = mutableSetOf<String>()
        }

        First["eps"] = mutableSetOf("eps")

        var changed = true
        while (changed) {
            changed = false

            productions.forEach { (nonTerminal, rules) ->
                rules.forEach { rule ->
                    val oldFirst = First[nonTerminal]!!.toSet()
                    var allEpsilon = true

                    for (symbol in rule) {
                        if (symbol in terminals || symbol == "eps") {
                            if (symbol != "eps") {
                                First[nonTerminal]!!.add(symbol)
                            }
                            allEpsilon = symbol == "eps"
                            break
                        } else {
                            First[nonTerminal]!!.addAll(First[symbol]!!.minus("eps"))
                            if ("eps" !in First[symbol]!!) {
                                allEpsilon = false
                                break
                            }
                        }
                    }

                    if (allEpsilon) {
                        First[nonTerminal]!!.add("eps")
                    }

                    if (First[nonTerminal]!! != oldFirst) {
                        changed = true
                    }
                }
            }
        }

        return this
    }


    fun generateFollow(): TableGenerator {
        nonTerminals.forEach {
            Follow[it] = mutableSetOf()
        }

        val startSymbol = productions.first().left
        Follow[startSymbol]!!.add("$")

        var changed = true
        while (changed) {
            changed = false

            for ((lhs, rules) in productions) {
                for (rule in rules) {
                    for ((index, symbol) in rule.withIndex()) {
                        if (symbol in nonTerminals) {
                            val followBefore = Follow[symbol]!!.toSet()

                            val nextSymbols = rule.drop(index + 1)

                            if (nextSymbols.isNotEmpty()) {
                                val firstOfNext = computeFirstOfSequence(nextSymbols)
                                Follow[symbol]!!.addAll(firstOfNext - "eps")

                                if ("eps" in firstOfNext) {
                                    Follow[symbol]!!.addAll(Follow[lhs]!!)
                                }
                            } else {
                                Follow[symbol]!!.addAll(Follow[lhs]!!)
                            }

                            if (Follow[symbol]!!.size > followBefore.size) {
                                changed = true
                            }
                        }
                    }
                }
            }
        }
        return this
    }


    private fun computeFirstOfSequence(symbols: List<String>): Set<String> {
        val result = mutableSetOf<String>()
        for (symbol in symbols) {
            val firstSet = First[symbol] ?: emptySet()
            result.addAll(firstSet - "eps")

            if ("eps" !in firstSet) {
                return result
            }
        }
        result.add("eps")
        return result
    }


    fun generateTable(): TableGenerator {
        createEmptyTable()

        productions.forEach { production ->
            val nonTerminal = production.left
            production.right.forEach { rule ->
                if (rule == listOf("eps")) {
                    Follow[nonTerminal]?.forEach { terminal ->
                        table[nonTerminal]?.get(terminal)?.add("eps")
                    }
                } else {
                    var canDeriveEps = true
                    for (symbol in rule) {
                        if (symbol in terminals) {
                            if (symbol != "eps") {
                                table[nonTerminal]?.get(symbol)?.add(rule.joinToString(" "))
                                canDeriveEps = false
                                break
                            }
                        } else if (symbol in nonTerminals) {
                            First[symbol]?.forEach { firstSymbol ->
                                if (firstSymbol != "eps") {
                                    table[nonTerminal]?.get(firstSymbol)?.add(rule.joinToString(" "))
                                }
                            }

                            if ("eps" !in First[symbol]!!) {
                                canDeriveEps = false
                                break
                            }
                        }
                    }
                    if (canDeriveEps) {
                        Follow[nonTerminal]?.forEach { terminal ->
                            table[nonTerminal]?.get(terminal)?.add(rule.joinToString(" "))
                        }
                    }
                }
            }
        }

        return this
    }

    private fun createEmptyTable() {
        nonTerminals.forEach { nonTerminal ->
            table[nonTerminal] = mutableMapOf()

            terminals.forEach { terminal ->
                table[nonTerminal]!![terminal] = mutableListOf()
            }
            table[nonTerminal]!!["$"] = mutableListOf()
        }
    }


    fun printLL1Table(filePath: String,pack: String) {

        val parseTable = table.map { (nonTerminal, terminalMap) ->
            nonTerminal to terminalMap.mapNotNull { (terminal, rules) ->
                if (rules.isNotEmpty()) {
                    terminal to rules
                } else {
                    null
                }
            }.toMap()
        }.toMap()


        val file = File(filePath)
        file.printWriter().use { writer ->
            writer.println("$pack\n")
            writer.println()
            writer.println("val Start = \"$start\"\n")
            writer.println("val GeneratedParseTable = mapOf<String, List<Map<String, List<String>>>>(")


            parseTable.forEach { (nonTerminal, terminalMap) ->
                writer.print("    \"$nonTerminal\" to listOf(")

                writer.println()
                writer.print("        mapOf(")
                terminalMap.forEach { (terminal, rules) ->
                    writer.print("\"$terminal\" to listOf(")
                    val list_rules = rules[0].split(" ")
                    writer.print(list_rules.joinToString(", ") { "\"$it\"" })
                    writer.println("),")
                }

                writer.println("    )),")
            }

            writer.println(")")
        }


    }

}
