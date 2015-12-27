cat training.txt | python mapper.py | sort | python reducer.py > weights.txt
python evaluate.py weights.txt test_data.txt test_labels.txt .