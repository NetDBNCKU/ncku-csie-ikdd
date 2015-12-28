import csv
import numpy
import copy

SPECI_FAMILY_VAR = (
    'Family_Hist_3', 'Family_Hist_5'
)

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    train_data = []

    with open('train.csv', newline='') as train_file:
        reader = csv.reader(train_file, delimiter=',')
        variable_names = reader.__next__()
        for row in reader:
            row_data = []
            for i in range(len(row)):
                # print(reader.line_num, i)
                if variable_names[i] in SPECI_FAMILY_VAR:
                    # merging two columns
                    if is_number(row[i]):
                        row_data[-1] += float(row[i])
                else:
                    if is_number(row[i]):
                        row_data.append(float(row[i]))
                    elif row[i] == '':
                        row_data.append(0.0)
                    else: # Convert Product_Info_2 to float value
                        row_data.append(float(int(row[i], 16)))
            train_data.append(row_data)
        for var in SPECI_FAMILY_VAR:
            variable_names.remove(var)

    correlation = numpy.corrcoef(train_data, rowvar=0)
    print('High correlation:')
    for i in range(len(variable_names)):
        for j in range(i + 1, len(variable_names)):
            if abs(correlation[i][j]) >= 0.8:
                print(str(i), variable_names[i], str(j), variable_names[j], sep=', ')
    print('Moderate correlation:')
    for i in range(len(variable_names)):
        for j in range(i + 1, len(variable_names)):
            if abs(correlation[i][j]) >= 0.3 and abs(correlation[i][j]) < 0.8:
                print(str(i), variable_names[i], str(j), variable_names[j], sep=', ')
    rank = copy.copy(variable_names)
    rank = sorted(rank, key=lambda x: abs(correlation[variable_names.index(x)][variable_names.index('Response')]))
    for var in rank:
        print(
            str(variable_names.index(var)),
            var,
            str(correlation[variable_names.index(var)][variable_names.index('Response')]),
            sep=', ')
