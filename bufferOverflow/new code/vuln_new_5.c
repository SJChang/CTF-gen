#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 64

void vuln() {
    char buf[BUFSIZE];
    char *secret_key = "SuperSecretKey";
    
    // Vulnerable gets() function allows overflowing the buffer 
    // and overwriting the secret_key pointer on the stack
    gets(buf);
    
    printf("Your input: %s\n", buf);
    
    // If the secret_key is modified to a specific value,
    // the program will reveal a "flag"
    if (strcmp(secret_key, "H4ck3rK3y") == 0) {
        printf("Access Granted! Here is your flag: CTF{St4ck_Sm4sh1ng_Succ3ss}\n");
    } else {
        printf("Access Denied. Wrong key.\n");
    }
}

int main() {
    // Disable buffering for stdout
    setbuf(stdout, NULL);
    
    printf("Enter the password: ");
    vuln();
    
    return 0;
}