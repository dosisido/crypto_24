#include<stdio.h>
#include<openssl/rand.h>
#include<string.h>

#define MAX 64

void printBuff(unsigned char* buffer, int size, char end_char){
    for(int i=0; i<size; i++){
        printf("%02x", buffer[i]);
        if(i != size-1) printf("%c", end_char);
    }
}

void getBuffFromString(unsigned char* buffer, unsigned char* str){
    int bufIndx = 0;
    int lenStr = strlen(str);
    for(int i = 0; i<lenStr; i+=3){
        sscanf(&str[i], "%2hhx-", &buffer[bufIndx]);
        bufIndx++;
    }
}

int main(int argc, char** argv){
    
    unsigned char rand1[MAX];
    unsigned char rand2[MAX];
    getBuffFromString(rand1, "63-3b-6d-07-65-1a-09-31-7a-4f-b4-aa-ef-3f-7a-55-d0-33-93-52-1e-81-fb-63-11-26-ed-9e-8e-a7-10-f6-63-9d-eb-92-90-eb-76-0b-90-5a-eb-b4-75-d3-a1-cf-d2-91-39-c1-89-32-84-22-12-4e-77-57-4d-25-85-98-");
    getBuffFromString(rand2, "92-05-d8-b5-fa-85-97-b6-22-f4-bd-26-11-cf-79-8c-db-4a-28-27-bb-d3-31-56-74-16-df-cb-f5-61-a7-9d-18-c2-63-92-f1-cb-c3-6d-2b-77-19-aa-21-07-8e-fe-8b-1a-4f-7d-70-6e-a4-7b-c8-68-30-43-12-50-30-1e-");
    
    unsigned char k1[MAX];
    unsigned char k2[MAX];
    unsigned char out[MAX];
    
    for(int i=0; i<MAX; i++){
        k1[i] = rand1[i] | rand2[i];
    }
    for(int i=0; i<MAX; i++){
        k2[i] = rand1[i] & rand2[i];
    }
    for(int i=0; i<MAX; i++){
        out[i] = k1[i] ^ k2[i];
    }

    printf("CRYPTO24{");
    printBuff(out, MAX, '-');
    printf("}\n");

}