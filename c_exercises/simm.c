#include <stdio.h>
#include <openssl/err.h>
#include <openssl/evp.h>

#define ENCRYPT 1
#define DECRYPT 0

#define KEY_FILE "simm_key.bin"
#define KEY_LEN_BYTE 16


void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char* argv[]){

    unsigned char key[KEY_LEN_BYTE];
    int i;

    FILE* fkey;
    if((fkey = fopen("./simm_key.bin", "r")) == NULL){
        fprintf(stderr, "Error in file opening");
        abort();
    }
    if(fread(key, 1, KEY_LEN_BYTE, fkey) != KEY_LEN_BYTE){
        fprintf(stderr, "Error reading key from file");
        abort();
    }
    fclose(fkey);

    printf("Key: \n\t");
    for(i=0; i<KEY_LEN_BYTE; i++)
        printf("%02x", key[i]);
    printf("\n");



    EVP_CIPHER_CTX* ctx;
    ctx = EVP_CIPHER_CTX_new();
    const int BUFF = 16;
    unsigned char buffer[BUFF];
    unsigned char out[BUFF + 16];
    int write;
    FILE* fin;
    FILE *fout;

    if(!EVP_CipherInit(ctx, EVP_aes_128_ecb(), key, NULL, ENCRYPT)) handle_errors();

    int n_read;
    if ((fin = fopen("./simm.c", "r")) == NULL){
        printf("Errore nell'apertura del file: \"%s\"", "./simm.c");
        exit(-1);
    }
    if ((fout = fopen("./enc.bin", "w")) == NULL){
        printf("Errore nell'apertura del file: \"%s\"", "./enc.bin");
        exit(-1);
    }

    while((n_read = fread(buffer, 1, BUFF, fin)) > 0){
        if(!EVP_CipherUpdate(ctx, out, &write, buffer, n_read)) handle_errors();
        if(fwrite(out, 1, write, fout) != write) handle_errors();
    }
    
    if(!EVP_CipherFinal_ex(ctx, out, &write)) handle_errors();
    if(fwrite(out, 1, write, fout) != write) handle_errors();
    printf("There\n");

    fclose(fout);
    fclose(fin);
    EVP_CIPHER_CTX_free(ctx);


    ctx = EVP_CIPHER_CTX_new();

    if(!EVP_CipherInit(ctx, EVP_aes_128_ecb(), key, NULL, DECRYPT)) handle_errors();
    
    if ((fin = fopen("./enc.bin", "r")) == NULL){
        printf("Errore nell'apertura del file: \"%s\"", "./enc.bin");
        exit(-1);
    }
    

    while((n_read = fread(buffer, 1, BUFF, fin)) > 0){
        if(!EVP_CipherUpdate(ctx, out, &write, buffer, n_read)) handle_errors();
        if(fwrite(out, 1, write, stdout) != write){
            fprintf(stderr, "Error writing decrypted data to stdout");
            abort();
        }
    }
    if(!EVP_CipherFinal_ex(ctx, out, &write)) handle_errors();
    if(fwrite(out, 1, write, stdout) != write){
        fprintf(stderr, "Error writing decrypted data to stdout");
        abort();
    }


    fclose(fin);
    EVP_CIPHER_CTX_free(ctx);

    
    return 0;
}