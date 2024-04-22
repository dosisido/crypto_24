#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <openssl/err.h>
#include <string.h>

#define MAXBUF 1024

#define KEY_LEN 18

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}



int main(int argc, char **argv){
       
    
    unsigned char key[] = "keykeykeykeykeykey";
    
    const EVP_MD* ALGO = EVP_sha256();

    if(argc != 3){
        fprintf(stderr,"Invalid parameters. Usage: %s filename1 filename2\n",argv[0]);
        exit(1);
    }


    FILE *f_in1;
    if((f_in1 = fopen(argv[1],"r")) == NULL) {
            fprintf(stderr,"Couldn't open the input file, try again\n");
            exit(1);
    }
    FILE *f_in2;
    if((f_in2 = fopen(argv[2],"r")) == NULL) {
            fprintf(stderr,"Couldn't open the input file, try again\n");
            exit(1);
    }


    //EVP_MD_CTX *EVP_MD_CTX_new(void);
    //pedantic mode? Check if md == NULL
    EVP_MD_CTX  *hmac_ctx = EVP_MD_CTX_new();

    //int EVP_DigestInit(EVP_MD_CTX *ctx, const EVP_MD *type);
    // int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *type, ENGINE *impl);
    // Returns 1 for success and 0 for failure.
    EVP_PKEY *hkey;
    hkey = EVP_PKEY_new_mac_key(EVP_PKEY_HMAC, NULL, key, KEY_LEN);

    if(!EVP_DigestSignInit(hmac_ctx, NULL, ALGO, NULL, hkey))
        handle_errors();

    size_t n;
    unsigned char buffer[MAXBUF];


    while((n = fread(buffer,1,MAXBUF,f_in1)) > 0){
    // Returns 1 for success and 0 for failure.
        if(!EVP_DigestSignUpdate(hmac_ctx, buffer, n))
            handle_errors();
    }
    while((n = fread(buffer,1,MAXBUF,f_in2)) > 0){
    // Returns 1 for success and 0 for failure.
        if(!EVP_DigestSignUpdate(hmac_ctx, buffer, n))
            handle_errors();
    }

    unsigned char hmac_value[EVP_MD_size(ALGO)];
    size_t hmac_len = EVP_MD_size(ALGO);

    //int EVP_DigestFinal_ex(EVP_MD_CTX *ctx, unsigned char *md, unsigned int *s);
    if(!EVP_DigestSignFinal(hmac_ctx, hmac_value, &hmac_len))
        handle_errors();

    // void EVP_MD_CTX_free(EVP_MD_CTX *ctx);
    EVP_MD_CTX_free(hmac_ctx);

    printf("The computed HMAC is: ");
    for(int i = 0; i < hmac_len; i++)
        printf("%02x", hmac_value[i]);
    printf("\n");


    // printf("The received HMAC is: %s\n",argv[2]);

    // // VERIFICATION PART
    // unsigned char hmac_binary[strlen(argv[2])/2];
    // for(int i = 0; i < strlen(argv[2])/2;i++){
    //     sscanf(&argv[2][2*i],"%2hhx", &hmac_binary[i]);
    // }

    // // if( CRYPTO_memcmp(hmac_binary, hmac_value, hmac_len) == 0 )
    // if( (hmac_len == (strlen(argv[2])/2)) && (CRYPTO_memcmp(hmac_binary, hmac_value, hmac_len) == 0))

    //         printf("Verification successful\n");
    // else
    //     printf("Verification failed\n");


	return 0;

}