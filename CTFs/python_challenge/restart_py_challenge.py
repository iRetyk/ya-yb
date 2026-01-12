### Run #2 of the python challenge from beginning
# Level 4 - "http://www.pythonchallenge.com/pc/def/linkedlist.php"
import urllib.request

nothing = "12345"
lst = [nothing]
for i in range(400):
    response = urllib.request.urlopen(f"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={nothing}")
    body_text = response.read().decode()
    nothing = body_text.split()[-1]
    if (i % 50) == 0:
        print(f"Iteration {i}: nothing = {nothing}")
    lst.append(nothing)

print(lst)