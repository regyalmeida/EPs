#include <stdio.h>
#include <stdlib.h>

int ** new_matrix(int n, int m){
    int ** matrix = (int **) malloc(n * sizeof(int *)); //aloca um vetor de ponteiros
    int i;
    
    for (i = 0; i <= n; i++) {  //percorre as linhas
        matrix[i] = (int *) malloc(m * sizeof(int)); //aloca um vetor de int para casa posicao do vetor de ponteiro
    }
    return matrix;
}

void change_position(int var1, int var2, int i, int** matrix){
    var2 = matrix[i][var1];
    matrix[i][var1] = matrix[i+1][var1];
    matrix[i+1][var1] = var2;
}

void sort(int n, int m, int c, int k, int p, int** matrix){
    int var2, var1;
    
    for(int j=0; j<=m; j++){
        for(int i=0; i<p; i++){
            if(i>=k){
                if(matrix[i][c] > matrix[i+1][c]){
                    for(var1=0; var1<m; var1++){
                        change_position(var1, var2, i, matrix);
                    }
                }
            }
        }
    }

    /* Imprimindo a matriz depois de ordenada */
    printf("Matriz ordenada pelas linhas a partir da original.\n");
    for(int i=0; i<n; i++){
        for(int j=0; j<
            m; j++){
            printf("%d  ", matrix[i][j]);
        }
        printf("\n");
    }
}



int main(int argc, const char* argv[]) {
    
    if (argc != 2) {
        printf("É necessário informar um, e apenas um parâmetro: endereço do arquivo de onde ler o grafo.\n");
        return EXIT_FAILURE;
    }
    
    int i;
    int n,m;
    int c,p,k;
    int ** matrix;
    int total;
    
    
    FILE * handler = fopen(argv[1], "r");
    if (!handler) {
        printf("Não foi possível abrir o arquivo '%s'. Certifique-se de que ele existe. \n", argv[1]);
        return 0;
    }
    
    /* lendo e armazenando valores do # linhas e # colunas */
    fscanf(handler, "%d %d", &n, &m);
    
    /* declaracao da matriz n x m */
    matrix = new_matrix(n, m);
    
    /* lendo e armazenando valores da coluna e linhas alvo */
    fscanf(handler, "%d %d %d", &c, &k, &p);
    
    total = n*m;
    
    int line, column, value;
    for (i=0; i < total; i++) {
        fscanf(handler, "%d %d %d", &line, &column, &value);
        matrix[line][column] = value;
    }
    sort(n, m, c, k, p, matrix);
}
