//
//  main.c
//  aed2-xavier-ep1
//
//  Created by Regiany Almeida on 03/09/17.
//  Copyright © 2017 Regiany Almeida. All rights reserved.
//


#include <stdbool.h>   /* variaveis bool assumem valores "true" ou "false" */ //MATRIZ ADJACENTE
#include <stdio.h>
#include <stdlib.h>

#define MAXNUMVERTICES 100

typedef int TipoPeso;
typedef struct MATRIZadj{
    int mat[MAXNUMVERTICES + 1][MAXNUMVERTICES + 1];
    int numVertices;
    int numArestas;
} MATRIZadj;
typedef int TipoApontador;

typedef struct estr {
    int v; // elemento
    struct estr *prox;
} NO;

// vertices do grafo - usado para criar o grafo
typedef struct {
    int flag; // para uso na busca em largura e profundidade, se necessario
    NO* inicio;
    int numero_arestas;
    int numero_vertices;
} VERTICE;


void inicializa_matriz(MATRIZadj *m, int nv) {
    int i, j;
    
    for (i=1; i<nv; i++){
        for (j=1; j<nv; j++){
            m->mat[i][j] = -1;
        }
    }
    m->numVertices = nv;
    m->numArestas = 0;
}

bool aresta_existe_matriz(MATRIZadj *m, int origem, int destino){
    if(m->mat[origem][destino] == 1)
        return true;
    
    return false;
}

void inserir_aresta_matriz(MATRIZadj* m, int linha, int coluna){
    if(!aresta_existe_matriz(m, linha, coluna))
        m->mat[linha][coluna] = 1;
}

void inicializa_grafo(VERTICE *g, int max){
    int i;
    for (i=1; i<=max; i++){
        g[i].inicio = NULL;
    }
}

bool aresta_existe_grafo(VERTICE *g, int origem, int destino){
    NO* p = g[origem].inicio;
    while(p){
        if(p->v == destino) return true;
        p = p->prox;
    }
    return false;
}

void inserir_aresta(VERTICE* g, int origem, int destino){
    if(aresta_existe_grafo(g, origem, destino)) return;
    
    NO* novo = (NO*)malloc(sizeof(NO));
    novo->v = destino;
    novo->prox = g[origem].inicio;
    g[origem].inicio = novo;
}

void matriz_para_lista(MATRIZadj *m, VERTICE **g){
    int origem, destino;
    
    for(origem = 1; origem<=m->numVertices; origem++){
        for(destino = 1; destino<=m->numVertices; destino++){
            if(aresta_existe_matriz(m, origem, destino)){
                inserir_aresta(*g, origem, destino);
            }
        }
    }
}
//Imprime o grafo em lista de adjancencia
void print_full(VERTICE* g, int n){
    int i;
    NO* tmp;
    for(i=1; i<=n; i++){
        tmp = g[i].inicio;
        printf("[%d]  |", i);
        while(tmp != NULL){
            printf("%d--->", tmp->v);
            tmp = tmp->prox;
        }
        printf("\n");
    }
    printf("\n");
}

int main(int argc, char *argv[]){

    FILE * arquivo = fopen(argv[1], "r");
    if (!arquivo) {
        printf("Não foi possível abrir o arquivo '%s'. Certifique-se de que ele existe. \n", argv[1]);
        return 0;
    }


    int i;
    int numero_vertices,numero_arestas;
    int linha, coluna, valor;

    /* lendo e armazenando valores do # vertices e # arestas */
    fscanf(arquivo, "%d %d", &numero_vertices, &numero_arestas);

    MATRIZadj* matriz = (MATRIZadj*)malloc(sizeof(MATRIZadj));
    VERTICE *grafo = (VERTICE*)malloc(sizeof(VERTICE) * (numero_vertices+1));
    VERTICE *grafoComplementar = (VERTICE*)malloc(sizeof(VERTICE) * (numero_vertices+1));

    /* declaracoes */
    inicializa_matriz(matriz, numero_vertices);
    inicializa_grafo(grafo, numero_vertices);
    inicializa_grafo(grafoComplementar, numero_vertices);
    
    
    
    for (i = 0; i < (numero_vertices*numero_vertices); i++) {
        fscanf(arquivo, "%d %d %d", &linha, &coluna, &valor);
        printf("%d, %d, %d \n", linha, coluna, valor);

        if(valor==1) inserir_aresta_matriz(matriz, linha, coluna);
        matriz_para_lista(matriz, &grafo);
        print_full(grafo, numero_vertices);
    }
}
