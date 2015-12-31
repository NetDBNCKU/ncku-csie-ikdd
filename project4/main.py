import csv
import numpy
import copy
from sklearn.neural_network import MLPClassifier

SPEC_CATA = (
    'Id',
    'Product_Info_2',
    'Response'
)
NUM_CONSIDERED_CATA = 37

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

considered_cata = []
with open('input/train.csv', newline='') as train_file:
    reader = csv.DictReader(train_file)
    train_input = []
    considered_cata = copy.copy(reader.fieldnames)
    considered_cata.remove('Id')
    for row in reader:
        train_input_row = []
        for cata in reader.fieldnames:
            if cata not in SPEC_CATA:
                if is_number(row[cata]):
                    train_input_row.append(float(row[cata]))
                else:
                    train_input_row.append(0.0)
            elif cata == 'Product_Info_2':
                train_input_row.append(float(int(row[cata], 16)))
            elif cata == 'Response':
                train_input_row.append(float(row[cata]))
        train_input.append(train_input_row)
    cor = numpy.corrcoef(train_input, rowvar=0)
    considered_cata = sorted(considered_cata, key=lambda x: -abs(cor[considered_cata.index(x)][-1]))
    considered_cata.remove('Response')
    while len(considered_cata) > NUM_CONSIDERED_CATA:
        considered_cata.pop()
    print(considered_cata)

clf = MLPClassifier(verbose=True)
with open('input/train.csv', newline='') as train_file:
    reader = csv.DictReader(train_file)
    train_input = []
    train_output = []

    for row in reader:
        train_input_row = []
        for cata in considered_cata:
            if cata not in SPEC_CATA:
                if is_number(row[cata]):
                    train_input_row.append(float(row[cata]))
                else:
                    train_input_row.append(0.0)
            elif cata == 'Product_Info_2':
                train_input_row.append(float(int(row[cata], 16)))
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
        for cata in considered_cata:
            if cata not in SPEC_CATA:
                if is_number(row[cata]):
                    predict_input_row.append(float(row[cata]))
                else:
                    predict_input_row.append(0.0)
            elif cata == 'Product_Info_2':
                predict_input_row.append(float(int(row[cata], 16)))
        predict_input.append(predict_input_row)
        predict_id.append(row['Id'])

    predict_output = clf.predict(predict_input)

    output_file.write('"Id","Response"')
    for i in range(len(predict_id)):
        output_file.write('\n' + predict_id[i] + ',' + str(predict_output[i]))
