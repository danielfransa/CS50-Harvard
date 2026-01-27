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
    for (int j = 0; j < i; j++)
    {
      printf("#");
    }
    printf("\n");
  }

  return 0;
}