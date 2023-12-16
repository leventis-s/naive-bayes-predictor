import csv

x_vals_y0 = {}
x_vals_y1 = {}
num_excluded = 1

with open("heart-train.csv") as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    # Find if there's a demographic section and exclude it (alongside y-values) in xi data accordingly
    if 'Demographic' in header:
        num_excluded = 2

    # First create empty dict
    for i in range(len(header) - num_excluded):
        x_vals_y0[i] = []
        x_vals_y1[i] = []
    for row in csvreader:
        y_val = row[len(row) - 1]
        # Get dict with all xi (except demographics) as keys and all corresponding vals in a list
        for i in range(len(row) - num_excluded):
            if y_val == '1':
                x_vals_y1[i].append(int(row[i]))
            else:
                x_vals_y0[i].append(int(row[i]))
    
num_y0 = len(x_vals_y0[0])
num_y1 = len(x_vals_y1[0])
p_y1 = (num_y1 + 1)/(num_y1 + num_y0 + 2)
p_y0 = (num_y0 + 1)/(num_y1 + num_y0 + 2)

# Now we have counted all the values and "completed training". Now we can test
with open("heart-test.csv") as f:
    csvreader = csv.reader(f)
    header = next(csvreader)
    guesses = []
    y_vals = []
    # Go over each example and give guess
    for row in csvreader:
        y_val = row[len(row) - 1]
        y_vals.append(int(y_val))
        x_vals = row[:-num_excluded]
        prob_y1 = p_y1
        prob_y0 = p_y0
        for i in range(len(x_vals)):
            xi = x_vals[i]
            if xi == '1':
                # Find how many examples where xi = 1 and y = 0 or 1
                num_xi1_y0 = sum(x_vals_y0[i])
                num_xi1_y1 = sum(x_vals_y1[i])
                # Use Laplace Prior
                prob_y0 *= ((num_xi1_y0 + 1)/(num_y0 + 2))
                prob_y1 *= ((num_xi1_y1 + 1)/(num_y1 + 2))
            else:
                # Find how many examples where xi = 0 and y = 0 or 1
                num_xi0_y0 = x_vals_y0[i].count(0)
                num_xi0_y1 = x_vals_y1[i].count(0)
                # Use Laplace formula
                prob_y0 *= ((num_xi0_y0 + 1)/(num_y0 + 2))
                prob_y1 *= ((num_xi0_y1 + 1)/(num_y1 + 2))
        guesses.append(int(prob_y1 > prob_y0))

    num_correct = 0
    # Find accuracy
    for guess, y_val in zip(guesses, y_vals):
        if guess == y_val:
            num_correct += 1
    print(num_correct/len(guesses))
        