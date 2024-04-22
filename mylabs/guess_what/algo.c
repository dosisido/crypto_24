#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#include<openssl/err.h>
#include<openssl/bn.h>

char* bignum1 = "00:9e:ee:82:dc:2c:d4:a0:0c:4f:5a:7b:86:63:b0:c1:ed:06:77:fc:eb:de:1a:23:5d:f4:c3:ff:87:6a:7d:ad:c6:07:fa:a8:35:f6:ae:05:03:57:3e:22:36:76:d5:0d:57:4f:99:f9:58:ad:63:7a:e7:45:a6:aa:fa:02:34:23:b6:9d:34:15:7b:11:41:b6:b1:ca:b9:1a:cd:29:55:bd:42:f5:04:ab:df:45:4a:9d:4e:ca:4e:01:f9:f8:74:59:67:ee:b6:a9:fb:96:b7:c0:94:00:17:8a:53:0e:b6:d8:31:c9:68:e6:64:38:d3:63:3a:04:d7:88:6b:f0:e1:ad:60:7f:41:bd:85:7b:d9:04:e1:97:5b:1f:9b:05:ce:ac:2c:c4:55:3f:b4:8b:89:4d:0a:50:9a:09:4e:5e:8f:5b:5f:55:69:72:5f:04:9b:3a:8a:09:b4:7f:8d:b2:ca:52:0e:5e:bf:f4:b0:ee:c9:ba:dc:93:4f:6d:d3:1f:82:1a:d9:fc:2c:a7:3f:18:23:0d:d7:44:c7:28:54:67:84:ee:73:92:65:f0:1c:e8:1e:6d:4d:95:65:b4:c8:4f:b8:04:62:58:2b:ee:32:64:a0:a7:dc:99:25:0e:50:53:76:bc:30:db:71:5e:93:d6:9f:1f:88:1c:76:5d:82:c8:59:39:51";
char* bignum2 = "00:d2:c6:01:32:6b:4c:4b:85:5f:52:7b:b7:8e:d6:8a:e4:c8:76:7e:6b:c9:24:9a:3e:ca:cd:2f:c9:b8:75:d4:f9:71:11:e1:cf:be:62:d3:2c:5f:f9:fd:9b:fa:ed:62:f3:df:44:c7:57:fb:ee:9b:b2:32:cb:54:49:29:6c:69:2e:30:1d:8c:1f:fa:b1:8e:e4:49:66:c1:fb:92:7c:82:ca:60:c9:40:a4:0a:b2:db:50:ec:f6:ff:98:a7:16:23:38:8d:06:d2:7c:a9:85:8a:c2:2b:4d:d4:e6:f1:89:e5:b0:42:54:a0:5f:3c:dd:c7:64:33:05:11:fb:ee:8b:26:07";

void handle_errors(){
    ERR_print_errors_fp(stderr);
    abort();
}

char carLower(char c){
    if(c >= 'A' && c <= 'Z'){
        return c + 32;
    }
    return c;
}

void strlower(char* in){
    // char* out = (char*)malloc(strlen(in));
    for(int i = 0; i < strlen(in); i++){
        in[i] = carLower(in[i]);
    }
}

void remove_colons(char* in, char*out){
    int i = 0, j = 0;
    while(in[i] != '\0'){
        if(in[i] != ':'){
            out[j] = in[i];
            j++;
        }
        i++;
    }
    out[j] = '\0';
}

void add_colons(char* in, char* out){
    int i = 0, j = 0;
    while(in[i] != '\0'){
        out[j] = in[i];
        j++;
        if(i % 2 == 1 && in[i+1] != '\0'){
            out[j] = ':';
            j++;
        }
        i++;
    }
    out[j] = '\0';
}

void reverseString(char* str, int effective_len){;
    for(int i = 0; i < effective_len/2; i++){
        char tmp = str[i];
        str[i] = str[effective_len-i];
        str[effective_len-i] = tmp;
    }
}

void nl(){
    printf("\n");
}

void print_BN_hex_colons(BIGNUM* bn, int desiredLen){
    char* hex = BN_bn2hex(bn);
    char* with_colons = (char*)malloc(strlen(hex)*10);
    add_colons(hex, with_colons);

    const int DEBUG = 0;
    
    if(desiredLen != 0){
        int thisLen = strlen(with_colons) -1;

        if(DEBUG) printf("%s", with_colons);
        if(DEBUG) nl();
        reverseString(with_colons, thisLen);
        if(DEBUG) printf("%s", with_colons);
        if(DEBUG) nl();

        for(thisLen++; thisLen < desiredLen; thisLen+=3){
            with_colons[thisLen]   = ':';
            with_colons[thisLen+1] = '0';
            with_colons[thisLen+2] = '0';
            with_colons[thisLen+3] = '\0';
            if(DEBUG) printf("%s", with_colons); 
            if(DEBUG) nl();
        }
        reverseString(with_colons, thisLen-1);
        with_colons[thisLen] = '\0';
        thisLen+=1;
    }

    strlower(with_colons);
    printf("%s", with_colons);
    free(with_colons);
    free(hex);
}

void print_BN_hex_colons_flag(BIGNUM* bn, int desiredLen){
    printf("CRYPTO24{");
    print_BN_hex_colons(bn, desiredLen);
    printf("}\n");
}

int main(int argc, char * argv[]){

    ERR_load_crypto_strings();

    const int len1 = strlen(bignum1)-1;
    const int len2 = strlen(bignum2)-1;
    char* BN1 = (char*)malloc(len1);
    char* BN2 = (char*)malloc(len2);
    remove_colons(bignum1, BN1);
    remove_colons(bignum2, BN2);
    char* buffer = (char*)malloc(len1 + len2 + 1);

    BIGNUM* a = BN_new();
    BIGNUM* b = BN_new();
    BIGNUM* res = BN_new();
    BIGNUM* res2 = BN_new();
    BN_CTX* ctx = BN_CTX_new();


    // -----------------------------------------------------------------


    BN_hex2bn(&a, BN1);
    BN_hex2bn(&b, BN2);

    // printf("BN1: %s\n", BN1);
    // printf("BN2: %s\n", BN2);

    // printf("%s\n", BN_bn2hex(a));
    // printf("%s\n", BN_bn2hex(b));

    // BN_print_fp(stdout, a); printf("\n");
    // BN_print_fp(stdout, b); printf("\n");

    int padding = 0;

    // BN_add(res, a, b);
    // print_BN_hex_colons_flag(res, padding);
    
    // BN_sub(res, a, b);
    // print_BN_hex_colons_flag(res, padding);
    
    // BN_mul(res, a, b, ctx);
    // print_BN_hex_colons_flag(res, padding);
    
    BN_div(res, res2, a, b, ctx);
    print_BN_hex_colons_flag(res, 0);
    print_BN_hex_colons_flag(res, len2);
    print_BN_hex_colons_flag(res, len1);


    // -----------------------------------------------------------------

    free(BN1);
    free(BN2);
    free(buffer);
    BN_free(a);
    BN_free(b);
    BN_free(res);
    BN_free(res2);
    BN_CTX_free(ctx);

    CRYPTO_cleanup_all_ex_data();
    ERR_free_strings();

}