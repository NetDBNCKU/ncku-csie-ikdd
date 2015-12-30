import csv
from sklearn.neural_network import MLPClassifier

CATA = (
    'BMI',
    'Wt',
    'Medical_History_23',
    'Medical_Keyword_15',
    'Medical_Keyword_3',
    'Medical_History_4',
    'Medical_History_39',
    'Ins_Age',
    'Product_Info_4'
)

with open('input/train.csv', newline='') as train_file:
    reader = csv.DictReader(train_file)
    clf = MLPClassifier(verbose=True)
    train_input = []
    train_output = []

    for row in reader:
        train_input_row = []
        for cata in CATA:
            train_input_row.append(float(row[cata]))
        train_input.append(train_input_row)
        train_output.append(int(row['Response']))

    clf.fit(train_input, train_output)

with\
    open('input/test.csv', newline='') as input_file,\
    open('output.csv', 'w') as output_file:

    reader = csv.DictReader(input_file)
    predict_input = []
    predict_id = []

    for row in reader:
        predict_input_row = []
        for cata in CATA:
            predict_input_row.append(float(row[cata]))
        predict_input.append(predict_input_row)
        predict_id.append(row['Id'])

    predict_output = clf.predict(predict_input)

    output_file.write('"Id","Response"')
    for i in range(len(predict_id)):
        output_file.write('\n' + predict_id[i] + ',' + str(predict_output[i]))
