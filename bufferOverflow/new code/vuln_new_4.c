#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 64
#define FLAGSIZE 64

char flag[FLAGSIZE];

void vuln() {
  char buf[BUFSIZE];
  int win = 0;

  printf("Enter your input: ");
  fflush(stdout);
  
  // Vulnerable gets() function allows overflowing the buffer
  gets(buf);

  // Buffer overflow can overwrite the 'win' variable
  if (win != 0) {
    printf("Congratulations! Here's your flag: %s\n", flag);
    fflush(stdout);
  } else {
    printf("Try again.\n");
  }
}

int main(int argc, char **argv) {
  FILE *f = fopen("flag.txt", "r");
  if (f == NULL) {
    printf("Please create 'flag.txt' in this directory with your own flag.\n");
    exit(0);
  }

  fgets(flag, FLAGSIZE, f);
  fclose(f);

  // Set the effective user id to the real user id
  // This prevents the program from running with elevated privileges
  setuid(getuid());

  // Call the vulnerable function
  vuln();

  return 0;
}