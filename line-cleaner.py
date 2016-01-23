with open('clean.csv', 'w') as output:
    for line in open('history-flight-joined-nobom.csv', 'r'):
        if '"' in line:
            if line.startswith('"') and line[1].isdigit():
                output.write("\n")
            output.write(line.strip())

flag = True
no_columns = -1
with open('fix.csv', 'w') as output:
    for line in open('clean.csv', 'r'):
        lines = line.strip().split(',')
        if flag:
            flag = False
            no_columns = len(lines)
            print no_columns
        else:
            lines = lines[:no_columns]
        output.write(','.join(lines) + '\n')
