import sys
import json

lang_list = ["java", "python", "c++"]
ver_list = ["old", 'new']
dict = {}

for lang in lang_list:
    for sample in range (5):
        for ver in ver_list:
            cost_sum = 0
            for trial in range (3):
                if lang == "java" and sample == 4 and ver == "old":
                    break
                
                path = f"claude-with-tools/{lang}/{sample+1}/a. claude-opus-4/{ver}_prompt/Trial{trial+1}.json"

                _f = path
                content = open(_f).read()

                #print(content)
                lines = content.split("\n")

                for line in lines[1:]:
                    if not line:
                        continue
                    #print(line)
                    obj = json.loads(line)

                    if "message" in obj: continue
                    cost = obj["modelUsage"]["claude-opus-4-20250514"]["costUSD"]
                    cost_sum += cost

            dict[f"{lang} {sample+1} {ver}"] = cost_sum/3

print(dict)
    


