package main

import (
	"fmt"
	"sort"
	"strings"
	"time"
)

func sao_anagramas(str1, str2 string) bool {
	return sortString(str1) == sortString(str2)
}

func sortString(s string) string {
	chars := strings.Split(s, "")
	sort.Strings(chars)
	return strings.Join(chars, "")
}

func main() {
	casos_teste := []struct {
		str1, str2 string
		esperado   bool
	}{
		{"roma", "amor", true},
		{"hello", "olleh", true},
		{"go", "golang", false},
		{"listen", "silent", true},
		{"triangle", "integral", true},
		{"python", "typhon", true},
		{"not", "anagram", false},
	}

	for _, caso := range casos_teste {
		inicio := time.Now()
		resultado := sao_anagramas(caso.str1, caso.str2)
		duracao := time.Since(inicio)

		fmt.Printf("'%s' e '%s' são anagramas: %v (esperado: %v) - Tempo: %v\n",
			caso.str1, caso.str2, resultado, caso.esperado, duracao)
	}
}
