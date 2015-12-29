import csv
import numpy

BITWISE = (1, 2, 4)
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
WEIGHTS = numpy.array([
    [-1.12686220e+01, -1.39567684e+01, -3.23780641e+00, 9.40543235e-01, -3.68576856e+00,
        1.80244929e+00, -1.26205222e+00, -1.19622626e+00, 1.02123045e-01, -1.00737370e-02],
    [-6.13184194e+00, -4.41444670e+01, -1.46754864e+01, 1.81682799e+00, -1.40288611e+00,
        -1.73983035e+01, 5.32772680e+00, 2.59248703e+00, -1.05295137e-01, -1.37229832e-02],
    [5.84553313e+00, -1.57922101e+01, 7.05992816e-01, 3.52226871e+00, 9.76185262e-01,
        -4.60139878e+00, 4.60552967e+00, 1.07789971e+00, -1.06220265e-01, -1.39438402e-02]
])

with open('test.csv', newline='') as input_file, open('output', 'w') as output_file:
    reader = csv.DictReader(input_file)
    output_file.write('"Id","Response"')
    for row in reader:
        output_file.write('\n' + row['Id'] + ',')
        response = 0
        v = [-1.0]
        for cata in CATA:
            v.append(float(row[cata]))
        v = numpy.array(v)
        for i in range(len(WEIGHTS)):
            dot_value = v.dot(WEIGHTS[i])
            if dot_value >= 0.0:
                response += BITWISE[i]
        output_file.write(str(response + 1))
