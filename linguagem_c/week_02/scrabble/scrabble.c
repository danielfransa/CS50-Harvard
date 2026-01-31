#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int get_score(string word);
void get_winner(int score_a, int score_b);

int main(void)
{
  string a = get_string("Player1: ");
  string b = get_string("Player2: ");

  int score_a = get_score(a);
  int score_b = get_score(b);

  get_winner(score_a, score_b);

  return 0;
}

// Get score for each player
int get_score(string word)
{
  int score = 0;

  for (int i = 0; i < strlen(word); i++)
  {
    if (isalpha(word[i]))
    {
      score += POINTS[tolower(word[i]) - 'a'];
    }
  }

  return score;
}

// Print the result of game!
void get_winner(int score_a, int score_b)
{
  if (score_a > score_b)
  {
    printf("Player 1 wins!\n");
  }
  else if (score_a < score_b)
  {
    printf("Player 2 wins!\n");
  }
  else
  {
    printf("Tie!\n");
  }
}