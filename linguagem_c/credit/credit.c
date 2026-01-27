#include <stdio.h>

int main(){
  long long card_number = 4003600000000014;
  int pick_number = 0;

  while(card_number > 0){
    int digit = card_number % 10;

      if (pick_number)
      {
        printf("%d\n", digit);
      }

    card_number /= 10;
    pick_number = !pick_number;
  }


  return 0;
}