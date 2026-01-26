#include <stdio.h>
#include <stdlib.h>

int main (){
  char name[20];

  printf("What's your name? ");
  fgets(name, 20, stdin);

  printf("Hello, %s\n", name);

  return 0;
}