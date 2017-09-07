//
//  main.c
//  aed2-xavier-ep1
//
//  Created by Regiany Almeida on 03/09/17.
//  Copyright © 2017 Regiany Almeida. All rights reserved.
//


#include <stdbool.h>   /* variaveis bool assumem valores "true" ou "false" */
#include <stdio.h>
#include <stdlib.h>

#define MAXNUMVERTICES 100

typedef struct MATRIZadj{
    int mat[MAXNUMVERTICES + 1][MAXNUMVERTICES + 1];
    int numVertices;
    int numArestas;
} MATRIZadj;

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

void inicializa_grafo(VERTICE *g, int max){
    int i;
    for (i=1; i<=max; i++){
        g[i].inicio = NULL;
    }
}

