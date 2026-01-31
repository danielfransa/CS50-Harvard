#include <stdio.h>

int main(){
  int change;
  int quarter;
  int dime;
  int nickel;
  int penny;

  do
  {
    printf("Change owed: ");
    scanf("%d", &change);
  } while (change < 1);

  do{
    if (change >= 25){
      change -= 25;
      quarter ++;
    }
    else if (change >=10){
      change -= 10;
      dime ++;
    }
    else if (change >=5){
      change -= 5;
      nickel ++;
    }
    else{
      change -= 1;
      penny ++;
    }
  } while (change > 0);

  int result = quarter + dime + nickel + penny;

  printf("%d", result);

  return 0;
}

