#include <stdio.h>
#include <string.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/rsa.h>

#define BLOCK 32

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}


int main(){

    int i, n_read, n_out;
    
    unsigned char rand1[BLOCK];
    unsigned char rand2[BLOCK];

    if(RAND_load_file("/dev/random", BLOCK) != BLOCK) {fprintf(stderr,"Error with rand init\n"); abort();}
    if(!RAND_bytes(rand1, BLOCK)) {fprintf(stderr,"Error with rand generation\n"); abort();}
    if(!RAND_bytes(rand2, BLOCK)) {fprintf(stderr,"Error with rand generation\n"); abort();}



    EVP_MD_CTX* ctx_dgst = EVP_MD_CTX_new();
    EVP_DigestInit(ctx_dgst, EVP_sha3_256());

    unsigned char msg[] = "my super secure message for the exercise";
    EVP_DigestUpdate(ctx_dgst, rand1, BLOCK);
    EVP_DigestUpdate(ctx_dgst, msg, strlen(msg));
    EVP_DigestUpdate(ctx_dgst, rand1, BLOCK);

    unsigned char key[BLOCK];
    EVP_DigestFinal(ctx_dgst, key, &n_out);
    if(n_out != BLOCK){
        fprintf(stderr, "Error in the digest final\n");
        abort();
    }

    EVP_MD_CTX_free(ctx_dgst);



    const int out_len = BLOCK + EVP_CIPHER_block_size(EVP_aes_256_ecb());
    unsigned char out[out_len];
    int len = 0;
    EVP_CIPHER_CTX* ctx_simm = EVP_CIPHER_CTX_new();
    EVP_CipherInit(ctx_simm, EVP_aes_256_ecb(), key, NULL, 1);

    if(!EVP_CipherUpdate(ctx_simm, out, &n_out, rand2, BLOCK)) handle_errors();
    len+= n_out;
    printf("len: %d; n_out: %d\n", len, n_out);
    if(!EVP_CipherFinal(ctx_simm, out + len, &n_out)) handle_errors();
    len+= n_out;
    printf("len: %d; n_out: %d; out_len: %d\n", len, n_out, out_len);

    EVP_CIPHER_CTX_free(ctx_simm);

    printf("The digest is: ");
    for(i = 0; i < len; i++)
        printf("%02x", out[i]);
    printf("\n");




    EVP_PKEY *keypair = NULL;
    int bits = 2048;
    if((keypair = EVP_RSA_gen(bits)) == NULL ) handle_errors();

    EVP_PKEY_CTX* ctx_rsa = EVP_PKEY_CTX_new(keypair, NULL);
    if (EVP_PKEY_encrypt_init(ctx_rsa) <= 0) {
        handle_errors();
    }

    size_t encrypted_msg_len;
    if (EVP_PKEY_encrypt(ctx_rsa, NULL, &encrypted_msg_len, out, out_len) <= 0) {
        handle_errors();
    }


    unsigned char encrypted_msg[encrypted_msg_len];
    if (EVP_PKEY_encrypt(ctx_rsa, encrypted_msg, &encrypted_msg_len, out, out_len) <= 0) {
        handle_errors();
    }

    EVP_PKEY_free(keypair);
    EVP_PKEY_CTX_free(ctx_rsa);

    printf("The rsa output is: ");
    for(i = 0; i < encrypted_msg_len; i++)
        printf("%02x", encrypted_msg[i]);
    printf("\n");

}