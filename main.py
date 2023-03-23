import pandas as pd
from math import pow


def loadData():
    df = pd.read_excel("CW2 Pumpkin Pie Data Sheet.xlsx")
    return df


def getGradePercentDF(df):
    percdb = {
        "State": [],
        "Total Pumpkins": [],
        "Grade 9%": [],
        "Grade 8%": [],
        "Grade 7%": [],
        "Grade 6%": [],
        "Grade 5%": [],
        "Grade 4%": [],
        "Grade 3%": [],
        "Grade 2%": [],
        "Grade 1%": [],
        "Grade 0%": [],
    }

    for indx, row in df.iterrows():
        percdb["State"].append(row[0])
        percdb["Total Pumpkins"].append(row[1])
        percdb["Grade 9%"].append(row[2]/100 * row[1])
        percdb["Grade 8%"].append((row[3] - row[2])/100 * row[1])
        percdb["Grade 7%"].append((row[4] - row[3])/100 * row[1])
        percdb["Grade 6%"].append((row[5] - row[4])/100 * row[1])
        percdb["Grade 5%"].append((row[6] - row[5])/100 * row[1])
        percdb["Grade 4%"].append((row[7] - row[6])/100 * row[1])
        percdb["Grade 3%"].append((row[8] - row[7])/100 * row[1])
        percdb["Grade 2%"].append((row[9] - row[8])/100 * row[1])
        percdb["Grade 1%"].append((row[10] - row[9])/100 * row[1])
        percdb["Grade 0%"].append((100 - row[10])/100 * row[1])

    return pd.DataFrame(percdb)


def getObservedTable(df):
    print(df)
    smoldf = df[["Total Pumpkins", "Grade 9%"]]
    smoldf.drop(smoldf.tail(1).index, inplace=True)
    return smoldf


def calculateExpectedTable(observed):
    expecteddb = {
        "Total Pumpkins": [],
        "Grade 9%": [],
    }

    columntotals = observed.sum(axis=0)
    rowtotals = observed.sum(axis=1)
    total = sum(rowtotals)
    print(total)

    for r in range(len(rowtotals)):
        for c in range(len(columntotals)):
            expecteddb[list(expecteddb.keys())[c]].append(rowtotals[r] * columntotals[c] / total)

    return pd.DataFrame(expecteddb)


def calculateChiSquaredTestStatistic(observed, expected):
    chiSqr = 0
    for r in range(len(observed.index)):
        for c in range(len(observed.columns)):
            value = pow(observed.values[r, c] - expected.values[r, c], 2) / expected.values[r, c]
            print(value)
            chiSqr += value
    return round(chiSqr, 3)


def main():
    df = loadData()
    percdf = getGradePercentDF(df)
    print(percdf)
    observed = getObservedTable(percdf)
    print("\n=== Observed ===\n" + str(observed))
    expected = calculateExpectedTable(observed)
    print(expected.sum())
    print("\n=== Expected ===\n" + str(expected))
    chiSqr = calculateChiSquaredTestStatistic(observed, expected)
    print("Chi Squared Test Statistic = " + str(chiSqr))
    dof = (observed.shape[0]-1) * (observed.shape[1]-1)
    print("Degrees of freedom = " + str(dof))
    critval = 18.493
    print("Critical vale = " + str(critval))
    if chiSqr <= 18.493:
        print("Test statistic is in range of critical value")
    else:
        print("Test statistic is out of range of the critical value")


if __name__ == "__main__":
    main()
