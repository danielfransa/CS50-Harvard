#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void rotation(string key, int n, string plaintext, char ciphertext[]);


int main(int argc, string argv[])
{
  if (argc == 1 || argc > 2)
  {
    printf("Usage: %s KEY\n", argv[0]);
    return 1;
  }

  int n = strlen(argv[1]);
  if (n != 26)
  {
    printf("Key must contain 26 characters.\n");
    return 1;
  }

  for (int i = 0; i < n; i++)
  {
    if (!isalpha(argv[1][i]))
    {
      printf("%c\n", argv[1][i]);
      printf("Key must only contain alphabetic characters.\n");
      return 1;
    }

    for (int j = i+1; j < n; j++)
    {
      if (tolower(argv[1][i]) == tolower(argv[1][j]))
      {
        printf("%c\n", argv[1][i]);
        printf("Key must not contain repeated characters.\n");
        return 1;
      }
    }
  }

  string plaintext = get_string("plaintext:  ");

  int m = strlen(plaintext);
  char ciphertext[m + 1];

  rotation(argv[1], m, plaintext, ciphertext);

  printf("ciphertext: %s\n", ciphertext);

  return 0;
}

void rotation(string key, int n, string plaintext, char ciphertext[])
{
  for (int i = 0; i < n; i++)
  {
    if (isupper(plaintext[i]))
    {
      int index = plaintext[i] - 'A';
      ciphertext[i] = toupper(key[index]);
    }
    else if (islower(plaintext[i]))
    {
      int index = plaintext[i] - 'a';
      ciphertext[i] =  tolower(key[index]);
    }
    else
    {
      ciphertext[i] = plaintext[i];
    }
  }
  ciphertext[n] = '\0';
}
