#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/bio.h>
#include <openssl/buffer.h>
#include <openssl/err.h>
#include <string.h>

#define BUF_SIZE 1024

#define STR_LEN 32 //  wc -c enc64.b

const char *encrypted_base64 = "ZZJ+BKJNdpXA2jaX8Zg5ItRola18hi95MG8fA/9RPvg=";
// base64 -d ./enc64 > enc64.b

const unsigned char key[] = "0123456789ABCDEF";
const unsigned char iv[] = "0123456789ABCDEF";

// Function to decode base64 encoded string
// char *base64_decode(const char *input, int length) {
//     BIO *bio, *b64;
//     BUF_MEM *bufferPtr;
//     char *buffer = (char *)malloc(length);
//     if (!buffer) return NULL;

//     bio = BIO_new_mem_buf((void *)input, length);
//     b64 = BIO_new(BIO_f_base64());
//     bio = BIO_push(b64, bio);

//     BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
//     BIO_read(bio, buffer, length);
//     BIO_free_all(bio);

//     return buffer;
// }

int base64_decode(const char *input, unsigned char *output) {
    BIO *bio, *b64;
    int decoded_len;

    // Create a BIO object with a Base64 filter
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_mem_buf(input, strlen(input)); // Read-only memory BIO

    // Link the BIO chain
    bio = BIO_push(b64, bio);

    // Decode
    decoded_len = BIO_read(bio, output, strlen(input));

    // Clean up
    BIO_free_all(bio);

    return decoded_len;
}

int tryAlgo(const char *algorithm_name, char *encrypted, int encrypted_len){
    // Setup decryption context
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        // printf("\tFailed to create decryption context.\n");
        return -4;
    }

    // Initialize decryption operation
    if (!EVP_CipherInit(ctx, EVP_get_cipherbyname(algorithm_name), key, iv, 0)) {
        // printf("\tCipher initialization failed.\n");
        return -3;
    }

    // Decrypt the data
    int len;
    unsigned char decrypted[BUF_SIZE];
    if (!EVP_CipherUpdate(ctx, decrypted, &len, (unsigned char *)encrypted, encrypted_len)) {
        // printf("\tDecryption failed.\n");
        return -2;
    }

    int decrypted_len = len;

    // Finalize decryption
    if (!EVP_CipherFinal(ctx, decrypted + len, &len)) {
        // printf("\tFinalization failed.\n");
        return -1;
    }

    decrypted_len += len;

    // Clean up
    EVP_CIPHER_CTX_free(ctx);

    // Null-terminate the decrypted data
    decrypted[decrypted_len] = '\0';

    // Build the flag
    printf("CRYPTO24{");
    for (int i = 0; i < decrypted_len; i++) {
        // printf("%02X", decrypted[i]);
        printf("%c", decrypted[i]);
    }
    printf("%s}\n", algorithm_name);

    return 0;
}

int main() {
    // Decryption parameters
    
    const char *algorithm_names[] = {
        "des-ecb",
        "des-ede",
        "des-ede3",
        "des-ede-ecb",
        "des-ede3-ecb",
        "des-cfb64",
        "des-cfb1",
        "des-cfb8",
        "des-ede-cfb64",
        "des-ede3-cfb64",
        "des-ede3-cfb1",
        "des-ede3-cfb8",
        "des-ofb",
        "des-ede-ofb",
        "des-ede3-ofb",
        "des-cbc",
        "des-ede-cbc",
        "des-ede3-cbc",
        "desx-cbc",
        "des-ede3-wrap",
        "idea-ecb",
        "idea-cfb64",
        "idea-ofb",
        "idea-cbc",
        "rc2-ecb",
        "rc2-cbc",
        "rc2-40-cbc",
        "rc2-64-cbc",
        "rc2-cfb64",
        "rc2-ofb",
        "bf-ecb",
        "bf-cbc",
        "bf-cfb64",
        "bf-ofb",
        "cast5-ecb",
        "cast5-cbc",
        "cast5-cfb64",
        "cast5-ofb",
        "rc5-32-12-16-cbc",
        "rc5-32-12-16-ecb",
        "rc5-32-12-16-cfb64",
        "rc5-32-12-16-ofb",
        "aes-128-ecb",
        "aes-128-cbc",
        "aes-128-cfb1",
        "aes-128-cfb8",
        "aes-128-cfb128",
        "aes-128-ofb",
        "aes-128-ctr",
        "aes-128-ccm",
        "aes-128-gcm",
        "aes-128-xts",
        "aes-128-wrap",
        "aes-128-wrap-pad",
        "aes-128-ocb",
        "aes-192-ecb",
        "aes-192-cbc",
        "aes-192-cfb1",
        "aes-192-cfb8",
        "aes-192-cfb128",
        "aes-192-ofb",
        "aes-192-ctr",
        "aes-192-ccm",
        "aes-192-gcm",
        "aes-192-wrap",
        "aes-192-wrap-pad",
        "aes-192-ocb",
        "aes-256-ecb",
        "aes-256-cbc",
        "aes-256-cfb1",
        "aes-256-cfb8",
        "aes-256-cfb128",
        "aes-256-ofb",
        "aes-256-ctr",
        "aes-256-ccm",
        "aes-256-gcm",
        "aes-256-xts",
        "aes-256-wrap",
        "aes-256-wrap-pad",
        "aes-256-ocb",
        "aes-128-cbc-hmac-sha1",
        "aes-256-cbc-hmac-sha1",
        "aes-128-cbc-hmac-sha256",
        "aes-256-cbc-hmac-sha256",
        "aria-128-ecb",
        "aria-128-cbc",
        "aria-128-cfb1",
        "aria-128-cfb8",
        "aria-128-cfb128",
        "aria-128-ctr",
        "aria-128-ofb",
        "aria-128-gcm",
        "aria-128-ccm",
        "aria-192-ecb",
        "aria-192-cbc",
        "aria-192-cfb1",
        "aria-192-cfb8",
        "aria-192-cfb128",
        "aria-192-ctr",
        "aria-192-ofb",
        "aria-192-gcm",
        "aria-192-ccm",
        "aria-256-ecb",
        "aria-256-cbc",
        "aria-256-cfb1",
        "aria-256-cfb8",
        "aria-256-cfb128",
        "aria-256-ctr",
        "aria-256-ofb",
        "aria-256-gcm",
        "aria-256-ccm",
        "camellia-128-ecb",
        "camellia-128-cbc",
        "camellia-128-cfb1",
        "camellia-128-cfb8",
        "camellia-128-cfb128",
        "camellia-128-ofb",
        "camellia-128-ctr",
        "camellia-192-ecb",
        "camellia-192-cbc",
        "camellia-192-cfb1",
        "camellia-192-cfb8",
        "camellia-192-cfb128",
        "camellia-192-ofb",
        "camellia-192-ctr",
        "camellia-256-ecb",
        "camellia-256-cbc",
        "camellia-256-cfb1",
        "camellia-256-cfb8",
        "camellia-256-cfb128",
        "camellia-256-ofb",
        "camellia-256-ctr",
    };
    int num_algorithms = sizeof(algorithm_names) / sizeof(algorithm_names[0]);

    // Decode the encrypted Base64 string
    char *encrypted = malloc(99999);
    // int enc_len =  base64_decode(encrypted_base64, encrypted);

    FILE* fin = fopen("enc64.b", "rb");
    fscanf(fin, "%s", encrypted);
    
    fread(encrypted, 1, STR_LEN, fin);

    fclose(fin);

    


    if (!encrypted) {
        printf("Base64 decoding failed.\n");
        return 1;
    }

    // Try to decrypt the data using each algorithm
    for (int i = 0; i < num_algorithms; i++) {
        if(tryAlgo(algorithm_names[i], encrypted, STR_LEN) == 0){
            printf("Current algorithm: %s\n", algorithm_names[i]);
        }
    }
    
    free(encrypted);
    return 0;
}
