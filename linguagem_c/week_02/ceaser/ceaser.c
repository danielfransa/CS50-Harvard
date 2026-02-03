#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void rotation(int key, int n, string plaintext, char ciphertext[]);


int main(int argc, string argv[])
{
  if (argc == 1 || argc > 2)
  {
    printf("Usage: %s key\n", argv[0]);
    return 1;
  }

  for (int i = 0, n = strlen(argv[1]); i < n; i++)
  {
    if(!isdigit(argv[1][i]))
    {
      printf("Usage: %s key\n", argv[0]);
      return 1;
    }
  }

  int key = atoi(argv[1]);

  string plaintext = get_string("plaintext:  ");

  int n = strlen(plaintext);
  char ciphertext[n + 1];

  rotation(key, n, plaintext, ciphertext);

  printf("ciphertext: %s\n", ciphertext);

  return 0;
}

void rotation(int key, int n, string plaintext, char ciphertext[])
{
  for (int i = 0; i < n; i++)
  {
    if (isupper(plaintext[i]))
    {
      ciphertext[i] = ((plaintext[i] - 'A' + key) % 26) + 'A';
    }
    else if (islower(plaintext[i]))
    {
      ciphertext[i] = ((plaintext[i] - 'a' + key) % 26) + 'a';
    }
    else
    {
      ciphertext[i] = plaintext[i];
    }
  }
  ciphertext[n] = '\0';
}
