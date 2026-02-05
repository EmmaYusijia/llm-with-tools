import sys
import json

_f = sys.argv[1]
content = open(_f).read()


#print(content)
lines = content.split("\n")
for line in lines[1:]:
    if not line:
        continue
    #print(line)
    obj = json.loads(line)

    if not "message" in obj: continue
    c = obj["message"]["content"][0]
    if "input" in c:
        print(c["name"], c["input"])


