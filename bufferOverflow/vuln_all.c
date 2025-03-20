#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG_SIZE 64

char flag[FLAG_SIZE];

void print_flag() {
    printf("FLAG: %s\n", flag);
}

void vuln() {
    char name[32];
    
    printf("Enter your name: ");
    gets(name); // Vulnerable gets() function allows buffer overflow
    
    printf("Hello, %s!\n", name);
}

int main(int argc, char **argv) {
    FILE *file = fopen("flag.txt", "r");
    if (file == NULL) {
        printf("Please create 'flag.txt' with your flag.\n");
        exit(0);
    }
    fgets(flag, FLAG_SIZE, file);
    fclose(file);

    char choice[4];
    while (1) {
        printf("\nMenu:\n");
        printf("1. Print your name\n");
        printf("2. Print the flag\n");
        printf("3. Quit\n");
        printf("Enter your choice: ");
        fgets(choice, 4, stdin);

        switch (choice[0]) {
            case '1':
                vuln(); // Call vulnerable function
                break;
            case '2':
                printf("Sorry, you are not authorized to view the flag.\n");
                break;
            case '3':
                printf("Goodbye!\n");
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}