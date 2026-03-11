while True:
  try:
    change = float(input("Change: "))
    if change >= 0:
      break
  except ValueError:
    pass

# convert to cents to avoid float errors
cents = round(change * 100)

count = 0

while cents > 0:
  if cents >= 25:
    cents -= 25
  elif cents >= 10:
    cents -= 10
  elif cents >= 5:
    cents -= 5
  else:
    cents -= 1
  count += 1

print(count)