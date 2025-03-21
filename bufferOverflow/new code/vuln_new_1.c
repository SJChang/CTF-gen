#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void login() {
  printf("You logged in successfully!\n");
  printf("Here's a secret flag: FLAG{buffer_overflow_master}\n");
}

void vuln() {
  char username[16];
  char password[16];
  
  printf("Enter username: ");
  gets(username); // Vulnerable gets() function allows overflowing username buffer
  
  printf("Enter password: ");
  gets(password); // Vulnerable gets() function allows overflowing password buffer
  
  printf("Username: %s\n", username);
  printf("Password: %s\n", password);
  
  if (strcmp(username, "admin") == 0 && strcmp(password, "secret_pass") == 0) {
    printf("Welcome, admin!\n");
    login();
  } else {
    printf("Invalid username or password.\n");
  }
}

int main() {
  printf("-- Simple Login Program --\n");
  vuln();
  return 0;
}

// The vulnerability is in the vuln() function, where gets() is used to read user input into fixed-size buffers.
// By entering a long string for the username or password, an attacker can overflow the buffers and overwrite data on the stack.
// To exploit this, an attacker needs to:
// 1. Overflow the username or password buffer to overwrite the return address on the stack.
// 2. Set the overwritten return address to the address of the login() function.
// 3. When vuln() returns, execution will jump to login(), printing the secret flag.
// This demonstrates a basic stack-based buffer overflow vulnerability.