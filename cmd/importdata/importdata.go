package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: ./importdata command [arguments]")
		os.Exit(1)
	}
}
