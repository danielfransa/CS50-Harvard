while True:
  try:
    h = int(input("Height: "))
    if 1 <= h <= 8:
      break
  except ValueError:
    pass

for i in range(1, h+1):
  print(" " * (h - i) + "#" * i + "  " + "#" * i)