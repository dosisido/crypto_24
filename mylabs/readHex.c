
#include <stdio.h>
#include <string.h>

#include <openssl/evp.h>


#define ENCRYPT 1
#define DECRYPT 0

int main()
{

//int EVP_EncryptInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, const unsigned char *key, const unsigned char *iv);
//int EVP_EncryptFinal(EVP_CIPHER_CTX *ctx, unsigned char *out, int *outl);

//  int EVP_DecryptInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, const unsigned char *key, const unsigned char *iv);
//  int EVP_DecryptFinal(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl);

//  int EVP_CipherInit(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type, const unsigned char *key, const unsigned char *iv, int enc);
//  int EVP_CipherFinal(EVP_CIPHER_CTX *ctx, unsigned char *outm, int *outl);




    

    unsigned char ciphertext_hex[] = "42279afcc3fddda4ebaafaa85c75920246e17cb060ab0567ecce7e740b5f956c403fb9860edd65a23c738be646baf324";

    
    // convert hexstring into bytes
    int ciphertext_len = strlen(ciphertext_hex)/2;
    unsigned char ciphertext_binary[ciphertext_len];
    for(int i = 0; i < ciphertext_len;i++){
        sscanf(&ciphertext_hex[2*i],"%2hhx", &ciphertext_binary[i]);
    }
    for(int i = 0; i < ciphertext_len; i++)
        printf("%02x", ciphertext_binary[i]);
    printf("\n");


    return 0;
}

