import csv
import numpy
import copy

SPECI_FAMILY_VAR = (
    'Family_Hist_3', 'Family_Hist_5'
)
MAX_NUM_VAR = 7
BITWISE = (1, 2, 4)
LEARNING_RATE = 0.01

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


if __name__ == '__main__':

    train_data = []

    # Loading training data
    with open('train.csv', newline='') as train_file:
        reader = csv.reader(train_file, delimiter=',')
        variable_names = reader.__next__()
        for row in reader:
            row_data = []
            for i in range(len(row)):
                if variable_names[i] in SPECI_FAMILY_VAR:
                    # Merging two columns
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
    print('Training data loaded')

    # Calculating correlation coefficient
    correlation = numpy.corrcoef(train_data, rowvar=0)
    # print('High correlation:')
    # for i in range(len(variable_names)):
    #     for j in range(i + 1, len(variable_names)):
    #         if abs(correlation[i][j]) >= 0.8:
    #             print(str(i), variable_names[i], str(j), variable_names[j], sep=', ')
    # print('Moderate correlation:')
    # for i in range(len(variable_names)):
    #     for j in range(i + 1, len(variable_names)):
    #         if abs(correlation[i][j]) >= 0.3 and abs(correlation[i][j]) < 0.8:
    #             print(str(i), variable_names[i], str(j), variable_names[j], sep=', ')

    # Filtering variables by correlation coefficient
    rank = list(range(len(variable_names)))
    rank.sort(key=lambda x: abs(correlation[x][variable_names.index('Response')]), reverse=True)
    rank.remove(variable_names.index('Response'))
    while len(rank) > MAX_NUM_VAR:
        rank.pop()

    # Initialize
    filtered_data = []
    response = []
    for row in train_data:
        filtered_row = [-1.0]
        response_row = []
        for var in rank:
            filtered_row.append(row[var])
        for bitwise in BITWISE:
            response_row.append(bool((int(row[variable_names.index('Response')]) - 1) & bitwise))
        filtered_data.append(filtered_row)
        response.append(response_row)
    filtered_data = numpy.array(filtered_data)

    weights = numpy.array([[0.0] + [1.0] * MAX_NUM_VAR] * len(BITWISE))

    while True:
        index_row = 0
        error_row = 0
        for row in filtered_data:
            index_weight = 0
            error_weight = len(BITWISE)
            for weight in weights:
                dot_value = row.dot(weight)
                if dot_value >= weight[0]:
                    if response[index_row][index_weight]:
                        error_weight -= 1
                    else:
                        weights[index_weight] = numpy.add(weight, numpy.multiply(row, LEARNING_RATE * -1.0))
                else:
                    if response[index_row][index_weight]:
                        weights[index_weight] = numpy.add(weight, numpy.multiply(row, LEARNING_RATE))
                    else:
                        error_weight -= 1
                index_weight += 1
            if error_weight:
                error_row += 1
            index_row += 1
        print(str(error_row), str(len(filtered_data)), sep='/')
        print(weights)
