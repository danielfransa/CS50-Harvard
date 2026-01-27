#include <stdio.h>

int main(){
  int h;

  do
  {
    printf("Height: ");
    scanf("%d", &h);
  } while (h<1 || h >8);

  printf("Height value is: %d\n", h);

  return 0;
}