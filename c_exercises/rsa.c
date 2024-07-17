#include <stdio.h>
#include <openssl/rsa.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <string.h>

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(){

    char msg[] = "message to encrypt with RSA";

    EVP_PKEY* keys;
    int bits = 2048;
    if(!(keys = EVP_RSA_gen(bits))) handle_errors();
    
    EVP_PKEY_CTX* ctx = EVP_PKEY_CTX_new(keys, NULL);
    if (EVP_PKEY_encrypt_init(ctx) <= 0) handle_errors();


    size_t encrypted_msg_len;
    if (EVP_PKEY_encrypt(ctx, NULL, &encrypted_msg_len, msg, strlen(msg)) <= 0) handle_errors();
    unsigned char encrypted_msg[encrypted_msg_len];
    if (EVP_PKEY_encrypt(ctx, encrypted_msg, &encrypted_msg_len, msg, strlen(msg)) <= 0) handle_errors();

    printf("Digest: \n\t");
    for(int i=0; i<encrypted_msg_len; i++)
        printf("%02x", encrypted_msg[i]);
    printf("\n");


    EVP_PKEY_free(keys);
    return 0;
}