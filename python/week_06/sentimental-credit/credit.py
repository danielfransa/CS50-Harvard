def validate_credit_card(card_number: str) -> str:
  total_sum = 0
  reverse_digits = card_number[::-1]

  for i, digit in enumerate(reverse_digits):
    n = int(digit)

    if i % 2 == 1:
      n *= 2
      if n > 9:
        n -= 9

    total_sum += n

  if total_sum % 10 != 0:
    return "INVALID"

  length = len(card_number)

  if length == 15 and card_number.startswith(("34", "37")):
    return "AMEX"
  elif length == 16 and card_number.startswith(("51", "52", "53", "54", "55")):
    return "MASTERCARD"
  elif length in (13, 16) and card_number.startswith("4"):
    return "VISA"
  else:
    return "INVALID"


def main():
  while True:
    card_input = input("Number: ")

    if card_input.isdigit():
      break

  print(validate_credit_card(card_input))

if __name__ == "__main__":
  main()