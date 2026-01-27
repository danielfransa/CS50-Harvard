#include <stdio.h>

int main(){
  long long card_number = 4003600000000014;

  while(card_number > 0){
    int digit = card_number % 10;

    printf("%d\n", digit);

    card_number /= 10;
  }


  return 0;
}