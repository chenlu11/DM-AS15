cat training.txt | python mapper.py | sort | python reducer.py > result.txt
python check.py result.txt duplicates.txt

b = 32
r = 32
TP = 83 FP = 0 FN = 7
Precision = 1.000000, recall = 0.922222, F1 = 0.959538

b = 50
r = 20
TP = 90 FP = 0 FN = 0
Precision = 1.000000, recall = 1.000000, F1 = 1.000000