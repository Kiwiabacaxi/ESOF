package main

import (
	"testing"
)

// Adicionando a função de benchmark
func BenchmarkSaoAnagramas(b *testing.B) {
	for i := 0; i < b.N; i++ {
		sao_anagramas("listen", "silent")
	}
}

func BenchmarkSaoAnagramasCurto(b *testing.B) {
	for i := 0; i < b.N; i++ {
		sao_anagramas("ab", "ba")
	}
}

func BenchmarkSaoAnagramasLongo(b *testing.B) {
	for i := 0; i < b.N; i++ {
		sao_anagramas("pneumonoultramicroscopicsilicovolcanoconiosis", "pneumonoultramicroscopicsilicovolcanoconiosis")
	}
}
