#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>
#include <openssl/err.h>


#define ENCRYPT 1
#define DECRYPT 0
#define MAX_BUFFER 1024

#define KEY "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
#define IV "11111111111111112222222222222222"
#define FILE_IN "file.enc.b"
#define FILE_OUT "flag.txt"

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

int main(int argc, char **argv){
    int tmp;
    

    int lenkey = strlen(KEY)/2;
    unsigned char key[lenkey];
    for(int i=0; i<lenkey; i++){
        sscanf(&KEY[i*2], "%2hhx", &key[i]);
    }

    int leniv = strlen(IV)/2;
    unsigned char iv[leniv];
    for(int i=0; i<leniv; i++)
        sscanf(&IV[i*2], "%2hhx", &iv[i]);


    // for(int i=0; i<lenkey; i++)
    //     printf("%02x", key[i]);
    // printf("\n");
    
    // for(int i=0; i<leniv; i++)
    //     printf("%02x", iv[i]);
    
    // printf("\n");

    FILE* fin;
    if((fin = fopen(FILE_IN, "r")) == NULL) abort();

    FILE* fout;
    if((fout = fopen(FILE_OUT, "w")) == NULL) abort();
    
    
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();

    EVP_CipherInit(ctx, EVP_chacha20(), key, iv, DECRYPT);

    unsigned char buffer[MAX_BUFFER];
    unsigned char flag[MAX_BUFFER];
    int length;
    int chunk_len;

    while((chunk_len = fread(buffer, 1, MAX_BUFFER, fin)) > 0){
        EVP_CipherUpdate(ctx, flag, &length, buffer, chunk_len);
        if(fwrite(flag, 1, length,fout) < length){
            fprintf(stderr,"Error writing the output file\n");
            abort();
        }
    }

    EVP_CipherFinal(ctx, flag, &length);
    if(fwrite(flag, 1, length,fout) < length){
        fprintf(stderr,"Error writing the output file\n");
        abort();
    }
    
    EVP_CIPHER_CTX_free(ctx);
    
    fclose(fin);
    fclose(fout);

    return 0;
}

