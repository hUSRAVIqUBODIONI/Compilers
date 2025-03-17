package main

import (
	"fmt"
	"go/ast"
	"go/format"
	"go/parser"
	"go/token"
	"os"
	"strings"
)

func replaceConstants(file *ast.File) {

	constValues := make(map[string]string)

	ast.Inspect(file, func(node ast.Node) bool {
		if genDecl, ok := node.(*ast.GenDecl); ok && genDecl.Tok == token.CONST {
			for _, spec := range genDecl.Specs {
				if valueSpec, ok := spec.(*ast.ValueSpec); ok && len(valueSpec.Values) > 0 {
					for i, name := range valueSpec.Names {
						if strings.HasSuffix(name.Name, "_") {
								if lit, ok := valueSpec.Values[i].(*ast.BasicLit); ok {
									constValues[name.Name] = lit.Value
									
								}
						}
					}
				}
			}
		}
		return true
	})

	fmt.Println("Constants map:",constValues)
	for key, value := range constValues {
		fmt.Printf("%s: %s\n", key, value)
	}

	var newDecls []ast.Decl
	for _, decl := range file.Decls {
		if assignStmt, ok := decl.(*ast.GenDecl); ok {
			if assignStmt.Tok == token.CONST {
				continue
			}
		}
		newDecls = append(newDecls, decl)
	}
	file.Decls = newDecls


	ast.Inspect(file, func(node ast.Node) bool {
		if ident, ok := node.(*ast.Ident); ok {
			if value, found := constValues[ident.Name]; found {
				fmt.Printf("Replacing %s with %s\n", ident.Name, value)
				*ident = *ast.NewIdent(value)
			}
		}
		return true
	})
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("usage: go run main.go <filename.go>")
		return
	}

	fset := token.NewFileSet()
	if file, err := parser.ParseFile(fset, os.Args[1], nil, parser.ParseComments); err == nil {
		replaceConstants(file)

		if err := format.Node(os.Stdout, fset, file); err != nil {
			fmt.Printf("Formatter error: %v\n", err)
		}
	} else {
		fmt.Printf("Errors in %s\n", os.Args[1])
	}
}

