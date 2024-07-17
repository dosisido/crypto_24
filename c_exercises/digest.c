#include <stdio.h>
#include <openssl/err.h>
#include <openssl/evp.h>

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(){

    FILE *fin;
    if ((fin = fopen("./digest.c", "r")) == NULL){
        printf("Errore nell'apertura del file: \"%s\"", "./digest.c");
        exit(-1);
    }
    
    unsigned char hash[EVP_MD_size(EVP_sha512())];
    int nout, nread, i;
    const int BUF = 16;
    unsigned char buffer[BUF];


    EVP_MD_CTX* ctx = EVP_MD_CTX_new();

    EVP_DigestInit(ctx, EVP_sha512());

    while((nread = fread(buffer, 1, BUF, fin)) > 0){
        
        if(!EVP_DigestUpdate(ctx, buffer, nread)) handle_errors();
    }

    if(!EVP_DigestFinal(ctx, hash, &nread)) handle_errors();
    if(nread != EVP_MD_size(EVP_sha512())){
        printf("Error in digest");
        abort();
    }

    EVP_MD_CTX_free(ctx);
    fclose(fin);

    printf("Digest: \n\t");
    for(i=0; i<nread; i++)
        printf("%02x", hash[i]);
    printf("\n");


    return 0;
}