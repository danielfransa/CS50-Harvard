#include <stdio.h>

int main(){
  int h;

  do
  {
    printf("Height: ");
    scanf("%d", &h);
  } while (h<1 || h >8);

  for (int i = 0; i < h; i++)
  {
    for (int j = h-1; j > i; j--)
    {
      printf(" ");
    }
    for (int k = 0; k < i+1; k++)
    {
      printf("#");
    }
    printf("\n");
  }

  return 0;
}