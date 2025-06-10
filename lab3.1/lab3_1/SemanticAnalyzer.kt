package com.example.lab

import com.example.lab.lab2_3.ASTNode
import com.example.lab.lab2_3.Token

class SemanticAnalyzer(val node: ASTNode) {

    val terminals = mutableSetOf<Token>()
    val nonterminals = mutableSetOf<Token>()
    val usedNonterminals = mutableSetOf<Token>()
    var lastNonterminal: Token? = null
    var isAlt: Boolean = false

    fun parseGrammarNode(){
        node.children.forEach { child ->
            when (child.label) {
                "GRAMMAR" -> parseGrammarNode()
                "TOKENS" -> parseTokensNode(child)
                "RULES" -> parseRulesNode(child)
                "START" -> parseStartNode(child)
            }
        }
        val extraNonTerms = usedNonterminals - nonterminals
        if (extraNonTerms.isNotEmpty()){
            println("Неопределенный нетерминал ${extraNonTerms.first()}")
            kotlin.system.exitProcess(1)

        }
    }

    // ------------ Собираем токены ------------- //
    private fun parseTokensNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "TOKEN" -> parseTokenNode(child)
                "TOKENS" -> parseTokensNode(child)
            }
        }

    }

    private fun parseTokenNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "name" ->  child.token?.let { terminals.add(it) }
                "TOKENLIST" -> parseTokenListNode(child)
            }
        }
    }

    private fun parseTokenListNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "name" -> child.token?.let { terminals.add(it) }
                "TOKENLIST" -> parseTokenListNode(child)
            }
        }

    }
    // -------------------------------------------- //




    // ------------ Разбираем правила ------------- //
    private fun parseRulesNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "UNIT" -> parseUnitNode(child)
                "UNITS" -> parseUnitsNode(child)
            }
        }

    }

    private fun parseUnitNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "name" -> {
                    if (child.token != null) {
                        if (lastNonterminal == null){lastNonterminal = child.token}
                        else if ((isAlt == false && lastNonterminal?.value == child.token.value)
                            || (isAlt == true && lastNonterminal?.value != child.token.value)){

                            println("Ошибка с окoнчанием правила для нетерминала: ${child.token}")
                            kotlin.system.exitProcess(1)
                        }
                        lastNonterminal = child.token
                        child.token.let{ nonterminals.add(it) }
                    }
                }
                "RULELIST" -> parseRuleListNode(child)
                "END" -> ParseEndNode(child)
            }
        }

    }

    private fun ParseEndNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "dot" -> {
                   isAlt = false
                }
                "comma" -> {
                    isAlt = true
                }

            }
        }

    }

    private fun parseRuleListNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "name" -> {if (child.token != null && !terminals.contains(child.token)) usedNonterminals.add(child.token)}
                "RULELIST" -> parseRuleListNode(child)
            }
        }

    }

    private fun parseUnitsNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "UNIT" -> parseUnitNode(child)
                "UNITS" -> parseUnitsNode(child)
            }
        }

    }

    // -------------------------------------------- //
    private fun parseStartNode(node: ASTNode){
        node.children.forEach { child ->
            when (child.label) {
                "name" -> {
                    if (!nonterminals.contains(child.token!!)) throw Throwable("Неопределенный Нетерминал для старта")
                }

            }
        }

    }

}

