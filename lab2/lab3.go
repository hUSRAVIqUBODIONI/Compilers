package main

import (
	"bufio"
	"fmt"
	"log"
	"os"

)

type WORD struct{
	word string
	pos int
}


func main() {
    // open file
    f, err := os.Open("test.txt")
    if err != nil {
        log.Fatal(err)
    }
    // remember to close the file at the end of the program
    defer f.Close()
	row , scanner :=0, bufio.NewScanner(f)

	
	//Words := []WORD{}
    for scanner.Scan() {

		runes := []rune(scanner.Text())
		word := ""
		for column := 0; column < len(runes) ; column++ {
			if runes[column] !=' ' {
				println(runes[column],string(runes[column]))
				word = word + string(runes[column])
				println(word)
			}else if runes[column] == ' ' && word != "" || runes[column] == '\n' {
				println("||||||||||||||")
				fmt.Println(word,"in pos ",column,row)
				word = ""
			}
			
		}
		row+=1
		fmt.Println()
		
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

	
	//fmt.Println(word+"abv")
}
