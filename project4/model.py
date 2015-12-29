import csv
import sys
import numpy
import copy

SPECI_FAMILY_VAR = (
    'Family_Hist_3', 'Family_Hist_5'
)
MAX_NUM_VAR = 9
BITWISE = (1, 2, 4)
LEARNING_RATE = 0.000000001

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

train_data = []

# Loading training data
with open('temp_csv/train.csv', newline='') as train_file:
    reader = csv.reader(train_file, delimiter=',')
    variable_names = reader.__next__()
    for row in reader:
        row_data = []
        for i in range(len(row)):
            # Merging two columns
            if variable_names[i] in SPECI_FAMILY_VAR:
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

weights = numpy.array([
    [-1.12686220e+01, -1.39567684e+01, -3.23780641e+00, 9.40543235e-01, -3.68576856e+00,
        1.80244929e+00, -1.26205222e+00, -1.19622626e+00, 1.02123045e-01, -1.00737370e-02],
    [-6.13184194e+00, -4.41444670e+01, -1.46754864e+01, 1.81682799e+00, -1.40288611e+00,
        -1.73983035e+01, 5.32772680e+00, 2.59248703e+00, -1.05295137e-01, -1.37229832e-02],
    [5.84553313e+00, -1.57922101e+01, 7.05992816e-01, 3.52226871e+00, 9.76185262e-01,
        -4.60139878e+00, 4.60552967e+00, 1.07789971e+00, -1.06220265e-01, -1.39438402e-02]
])
best = 59381
best_weights = copy.copy(weights)

while True:

    error_row = 0
    index_row = 0
    for row in filtered_data:
        index_weight = 0
        for weight in weights:
            dot_value = row.dot(weight)
            if dot_value >= 0.0:
                if response[index_row][index_weight]:
                    pass
                else:
                    weights[index_weight] = numpy.add(weight, numpy.multiply(row, LEARNING_RATE * -1.0))
            else:
                if response[index_row][index_weight]:
                    weights[index_weight] = numpy.add(weight, numpy.multiply(row, LEARNING_RATE))
                else:
                    pass
            index_weight += 1
        index_weight = 0
        error_weight = len(BITWISE)
        for weight in best_weights:
            dot_value = row.dot(weight)
            if dot_value >= 0.0:
                if response[index_row][index_weight]:
                    error_weight -= 1
                else:
                    pass
            else:
                if response[index_row][index_weight]:
                    pass
                else:
                    error_weight -= 1
            index_weight += 1
        if error_weight:
            error_row += 1
        index_row += 1

    # if error_row < best:
    print(str(error_row), str(len(filtered_data)), sep='/')
    print(best_weights)
    sys.stdout.flush()
    best = error_row

    best_weights = copy.copy(weights)
