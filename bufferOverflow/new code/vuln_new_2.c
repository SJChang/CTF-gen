#include <stdio.h>
#include <string.h>

void vuln() {
    char buffer[64];
    
    // Vulnerability: Using gets() to read user input into a fixed-size buffer
    // Exploitation: Provide an input longer than 64 characters to overflow the buffer
    // and overwrite the return address on the stack. This allows for execution of 
    // arbitrary code by redirecting the program flow to a memory address controlled
    // by the attacker.
    gets(buffer);
    
    printf("You entered: %s\n", buffer);
}

void print_flag() {
    // This function is never called during normal execution
    printf("Congratulations! You have successfully exploited the buffer overflow vulnerability.\n");
    printf("Here is your flag: OVERFLOW_MASTER\n");
}

int main() {
    printf("Welcome to the Buffer Overflow Challenge!\n");
    printf("Enter your input: ");
    
    vuln();
    
    printf("Thank you for participating!\n");
    
    return 0;
}