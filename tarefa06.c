// Escreva um programa em C que faça a multiplicação de matrizes (100x100) 
// usando apenas índices. Escreva em segundo programa em C que faça as 
// mesmas operações, mas que use ponteiros e aritmética de ponteiros para a 
// função de mapeamento de armazenamento para fazer as referências aos 
// elementos da matriz. Compare a eficiência em termos de tempo dos dois programas. 
// Qual dos dois é mais confiável. Por quê?

// A aritmética de ponteiros se mostrou mais rápida, uma das explicações é que o
// C trabalha de forma mais rápida com endereços de memória (ponteiros), pois ele
// pode apontar para qualquer local da memória. Quando é feito a declaração
// usando o índice ele vai precisar buscar qual é o endereço de memória desse elemento, o
// que leva algum tempo.

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#define MAX 100


void preencher_matriz(int matriz[MAX][MAX]);
void multiplicar(int matrizA[MAX][MAX], int matrizB[MAX][MAX], int matrizC[MAX][MAX]);
void ponteiro_multiplicar(int matrizA[MAX][MAX], int matrizB[MAX][MAX], int matrizC[MAX][MAX]);
void mostrar_matriz(int matriz[MAX][MAX], char c);


int main(int argc, char **argv){
    int matrizA[MAX][MAX], matrizB[MAX][MAX], matrizC[MAX][MAX];
    char a = 'A', b = 'B', c = 'C';

    srand(time(NULL));
    
    preencher_matriz(matrizA);
    preencher_matriz(matrizB);

    // mostrar_matriz(matrizA, a);
    // mostrar_matriz(matrizB, b);

    multiplicar(matrizA, matrizB, matrizC);
    ponteiro_multiplicar(matrizA, matrizB, matrizC);

    return 0;
}

void preencher_matriz(int matriz[MAX][MAX]){
    int i, j;

    for(i=0; i<MAX; i++){
        for(j=0; j<MAX; j++){
            matriz[i][j] = rand() % 100 + 1;
        }
    }
}

void multiplicar(int matrizA[MAX][MAX], int matrizB[MAX][MAX], int matrizC[MAX][MAX]){
    int i, j, x;

    clock_t begin = clock();

    for(i=0; i<MAX; i++){
        for(j=0; j<MAX; j++){
            matrizC[i][j] = 0;
            for(x=0; x<MAX; x++){
                matrizC[i][j] += (matrizA[i][x] * matrizB[x][j]);
            }
        }
    }

    clock_t end = clock();
    printf("Multiplicar\nTempo: %f\n\n", (double)(end - begin) / CLOCKS_PER_SEC);
}

void ponteiro_multiplicar(int matrizA[MAX][MAX], int matrizB[MAX][MAX], int matrizC[MAX][MAX]){
    int i, j, x;

    clock_t begin = clock();

    for(i=0; i<MAX; i++){
        for(j=0; j<MAX; j++){
            matrizC[i][j] = 0;
            for(x=0; x<MAX; x++){
                matrizC[i][j] += (*(*(matrizA + i) + x) * *(*(matrizB + x) + j));
            }
        }
    }

    clock_t end = clock();
    printf("Aritmética de Ponteiros\nTempo: %f\n\n", (double)(end - begin) / CLOCKS_PER_SEC);
}

void mostrar_matriz(int matriz[MAX][MAX], char c){
    int i, j;

    printf("Matriz %c\n", c);

    for(i=0; i<MAX; i++){
        for(j=0; j<MAX; j++){
            printf("matriz[%d][%d] = %d\n", i, j, matriz[i][j]);
        }
    }
    printf("=======\n");
}
