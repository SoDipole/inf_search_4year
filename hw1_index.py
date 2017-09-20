from collections import defaultdict
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

collection = [
    ["У", "меня", "болит", "голова"],
    ["Сегодня", "слишком", "жарко"],
    ["Голову", "с", "плеч"]]

index = defaultdict(list)

i = 1
for document in collection:
    for token in document:
        index[morph.parse(token)[0].normal_form].append(i)
    i += 1

print(sorted(index.items()))