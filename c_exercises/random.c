#include <stdio.h>
#include <openssl/rand.h>
#include <openssl/err.h>

#define RAND 16

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(){
    
    unsigned char random[RAND];
    int i;


    const int CHUNK = 16;
    for(i=0; i<RAND; i+=CHUNK){
        if(RAND_load_file("/dev/random", CHUNK) != CHUNK) handle_errors();
        if(!RAND_bytes(random + i, CHUNK)) handle_errors();
    }

    printf("Sequence: \n\t");
    for(i=0; i<RAND; i++)
        printf("%02x", random[i]);
    printf("\n");

    int n_write = 0;
    FILE* fout;
    if((fout = fopen("./simm_key.bin", "w")) == NULL){
        printf("Error in file opening");
        abort();
    } 

    if(fwrite(random, 1, RAND, fout) != RAND){
        printf("Error writing in the output file\n");
        abort();
    }


    fclose(fout);
    return 0;
}