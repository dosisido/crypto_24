#include<stdio.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>

#define FILE_IN "file.txt"
#define SECRET "this_is_my_secret"
#define MAXBUF 1024


int main(){

    FILE *f_in;
    if((f_in = fopen(FILE_IN,"r")) == NULL) {
        fprintf(stderr,"Couldn't open the input file, try again\n");
        exit(1);
    }


    EVP_MD_CTX *md = EVP_MD_CTX_new();

    EVP_DigestInit(md, EVP_sha512());

    EVP_DigestUpdate(md, SECRET, strlen(SECRET));

    int n;
    unsigned char buffer[MAXBUF];
    while((n = fread(buffer,1,MAXBUF,f_in)) > 0){
        EVP_DigestUpdate(md, buffer, n);
    }

    EVP_DigestUpdate(md, SECRET, strlen(SECRET));


    unsigned char md_value[EVP_MD_size(EVP_sha512())];
    int md_len;

    EVP_DigestFinal_ex(md, md_value, &md_len);

    EVP_MD_CTX_free(md);

    printf("The digest is: ");
    printf("CRYPTO24{");
    for(int i = 0; i < md_len; i++)
        printf("%02x", md_value[i]);
    printf("}\n");

}