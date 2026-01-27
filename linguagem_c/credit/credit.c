#include <stdio.h>
#include <string.h>
#include <ctype.h>

char* validate_credit_card(long long card_number);

int main(){
  char input[32];
  long long card_number;
  int valido;

  do {
    valido = 1;

    printf("Number: ");
    scanf("%31s", input);

    for (int i = 0; input[i] != '\0'; i++) {
      if (!isdigit(input[i])) {
        valido = 0;
        break;
      }
    }

    if (valido) {
      sscanf(input, "%lld", &card_number);
    }
  } while (!valido);


  printf("%s\n", validate_credit_card(card_number));

  return 0;
}

char* validate_credit_card(long long card_number){
  int pick_number = 0;
  int sum = 0;

  long long number = card_number;

  while(number > 0){
    int digit = number % 10;

      if (pick_number)
      {
        digit *= 2;
        if (digit > 9){
          digit -= 9;
        }
      }

    sum += digit;
    number /= 10;
    pick_number = !pick_number;
  }

  if(sum % 10 != 0){
    return "INVALID";
  }

  long long starts = card_number;

  while (starts >= 100){
    starts /= 10;
  }

  if (starts == 34 || starts == 37){
    return "AMEX";
  }
  else if (starts == 51 || starts == 52 || starts == 53 || starts == 54 || starts == 55){
    return "MASTERCARD";
  }
  else
  {
    while (starts >= 10){
      starts /= 10;
    }

    if (starts == 4){
      return "VISA";
    }
    else{
      return "INVALID";
    }
  }

}