package com.example.lab
import java.io.File

data class ParseTreeNode(
    val label: String,
    val children: MutableList<ParseTreeNode> = mutableListOf()
)

fun generateDotString(root: ParseTreeNode): String {
    val builder = StringBuilder()
    builder.append("digraph ParseTree {\n")
    builder.append("node [shape=box];\n")

    var id = 0
    val nodeIds = mutableMapOf<ParseTreeNode, String>()

    fun addNode(node: ParseTreeNode): String {
        val nodeId = "node${id++}"
        nodeIds[node] = nodeId
        builder.append("$nodeId [label=\"${node.label}\"];\n")
        return nodeId
    }

    fun traverse(node: ParseTreeNode): String {
        val currentId = addNode(node)
        for (child in node.children) {
            val childId = traverse(child)
            builder.append("$currentId -> $childId;\n")
        }
        return currentId
    }

    traverse(root)

    builder.append("}\n")
    return builder.toString()
}
