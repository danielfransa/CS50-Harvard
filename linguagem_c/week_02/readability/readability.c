#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int get_letters(string text);
int get_words(string text);
int get_sentences(string text);


int main(void)
{
  string text = get_string("Text: ");


  int letters = get_letters(text);
  int words = get_words(text);
  int sentences = get_sentences(text);

  //Get Coleman-Liau index
  float L = (letters / (float) words)*100;
  float S = (sentences / (float) words)*100;

  float index = 0.0588 * L - 0.296 * S - 15.8;

  // return grade to user...
  int grade = round(index);

  if (grade < 1)
  {
    printf("Before Grade 1\n");
  }
  else if (grade >= 1 && grade <= 16)
  {
    printf("Grade %i\n", grade);
  }
  else
  {
    printf("Grade 16+\n");
  }

  return 0;
}

int get_letters(string text)
{
  int letters = 0;

  for (int i = 0, n = strlen(text); i < n; i++)
  {
    if (isalpha(text[i]))
    {
      letters++;
    }
  }
  return letters++;
}

int get_words(string text)
{
  int words = 0;
  int is_char = 0;

  for (int i = 0, n = strlen(text); i < n; i++)
  {
    if (!isspace(text[i]) && is_char == 0)
    {
      words++;
      is_char = 1;
    }
    else if (isspace(text[i]))
    {
      is_char = 0;
    }
  }

  return words;
}

int get_sentences(string text)
{
  int sentences = 0;

  for (int i = 0, n = strlen(text); i < n; i++)
  {
    if (text[i] == '!')
    {
      sentences++;
    }
    else if (text[i] == '?')
    {
      sentences++;
    }
    else if (text[i] == '.' && text[i-1] != '.')
    {
      sentences++;
    }
  }

  return sentences;
}