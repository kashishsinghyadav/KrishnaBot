with open("sbg.txt", "r", encoding="utf-8") as f:
    for _ in range(200):  # Print first 200 lines
        print(f.readline().strip())
