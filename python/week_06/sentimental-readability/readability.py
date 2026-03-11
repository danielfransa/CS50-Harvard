def main():
  text = input("Text: ")

  letters = sum(1 for c in text if c.isalpha())
  words = len(text.split())
  sentences = sum(1 for c in text if c in ".!?")

  L = (letters / words) * 100
  S = (sentences / words) * 100

  index = 0.0588 * L - 0.296 * S - 15.8
  grade = round(index)

  if grade < 1:
    print("Before Grade 1")
  elif grade <= 16:
    print(f"Grade {grade}")
  else:
    print("Grade 16+")


if __name__ == "__main__":
  main()