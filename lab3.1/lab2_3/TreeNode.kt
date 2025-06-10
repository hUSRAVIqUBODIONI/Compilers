package com.example.lab.lab2_3

class DotGenerator {
    private var nodeIdCounter = 0
    fun generateDotString(root: ASTNode): String {
        val builder = StringBuilder()
        builder.append("digraph ParseTree {\n")
        builder.append("node [shape=box];\n")

        val nodeIds = mutableMapOf<ASTNode, String>()


        fun addNode(node: ASTNode): String {
            val nodeId = "node${nodeIdCounter++}"
            nodeIds[node] = nodeId
            builder.append("$nodeId [label=\"${node.label}\"];\n")
            return nodeId
        }

        fun traverse(node: ASTNode): String {
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
}



data class ASTNode(
    val label: String,
    val children: MutableList<ASTNode> = mutableListOf(),
    val token: Token? = null
)
