import re
import io
import pandas as pd
import numpy as np

def grading_engine(infile, outfile, obj, proc):
    
    obj = [float(i) for i in obj if float(i)>0]
    proc = [float(i) for i in proc if float(i)>0]

    
    if sum(obj) != 1 or sum(proc)!= 1:
        return "Course Objective/Process does not sum to 1"
    else:
        return grading_points(infile, outfile, obj, proc)


def generate_grading(score, mm, nn):
    m = len(mm)
    n = len(nn)

    grading = np.zeros((m, n), float)

    for i in range(0, m):
        for j in range(0, n):
            grading[i][j] = mm[i] * nn[j] * 100

    print(grading)

    grading = grading.reshape(m * n, order='C')
    weight = np.cumsum(grading)
    # weight = np.reshape(weight, (m, n), order='C')

    print(weight)

    while True:
        if np.sum(grading) <= score + 0.05:
            break

        rint = np.random.randint(0, 100)

        for i in range(0, m * n):
            if rint <= weight[i] and grading[i] >= 0.5:
                grading[i] = grading[i] - 0.5
                break

    grading = grading.reshape((m, n), order='C')

    print(grading)
    print(np.sum(grading))

    # return grading
    return np.sum(grading)


for i in range(0, 10000):
    score = np.random.randint(30, 100)
    print(score)
    if np.fabs(score - generate_grading(score, [0.1, 0.1, 0.4, 0.4], [0.25, 0.25, 0.2, 0.3])) > 1e-4:
        print('------------------------')
        break


def grading_points(infile, outfile, mm, nn):
    pd.set_option('display.notebook_repr_html', False)
    sheet = pd.read_excel(io=infile, sheet_name=0, engine='openpyxl')

    sheet = pd.DataFrame.dropna(sheet)

    Score = sheet['Score']
    Name = sheet['Name']
    Number = sheet['NO']

    print(sheet)
    # print(sheet['Score'])
    # print(len(sheet))

    # mm = [0.3, 0.3, 0.2, 0.2]
    # nn = [0.2, 0.2, 0.2, 0.2, 0.2]

    # for score in Score:
    #     # print(score)
    #     gradings.append(generate_grading(score, mm, nn))

    output = list()

    for i in range(0, len(sheet)):
        grading = generate_grading(Score[i], mm, nn)
        header = f"{Number[i]}\t{Name[i]}\t{Score[i]}\t{np.sum(grading):.1f}"
        output.append(header)

        # bio = io.BytesIO()
        # np.savetxt(bio, gradings[i], fmt="%.1f")
        # output.append(bio.getvalue().decode('latin1'))
        # output.append("\n")
        # bio.close()

        for row in grading:
            temp = [f"{col:.1f}" for col in row]
            temp = '\t'.join(temp)
            output.append("Objective:\t" + temp)

        output.append('')

    with open(outfile, 'w') as file:
        file.write('\n'.join(output).expandtabs(16))

    # print('\n'.join(output).expandtabs(16))
    
    return None
    

#grading_points('./files/grading.xlsx', 'test_grading.txt', [0.5, 0.5], [0.5, 0.5])


# for item in gradings:
#     # print(np.array2string(item))
#     # print(' '.join(str([col for row in item for col in row])))
#     bio = io.BytesIO()
#     np.savetxt(bio, item, fmt="%.1f")
#     output.append(bio.getvalue().decode('latin1'))
#     bio.close()
#     # mystr = re.sub('[\[\]]', '', np.array_str(item))
#     # print(mystr)
#     # output.append()
