from sympy import *

def calcTeamOpr():
    #mkspexec.txt here
    t11212, t10092, t12345 = symbols("t11212 t10092 t12345")
    equations = [Eq(t11212 + t10092, 540), Eq(t12345 + t10092, 530), Eq(t12345 + t11212, 505), ]

    teamopr = solve(equations)
    return teamopr

def SortListInList(list):
    newList = []
    for i in range(len(list)):
        low = 0
        high = len(newList) - 1
        while low <= high:
            middle = (high + low) / 2
            if list[i][1] == newList[middle][1]:
                low = middle
                break
            elif list[i][1] > newList[middle][1]:
                low = middle + 1
            elif list[i][1] < newList[middle][1]:
                high = middle - 1

        newList.insert(low, list[i])

    goodList = []
    for i in range(len(newList)-1,-1,-1):
        goodList.append(newList[i])

    return goodList

def main():
    teamoprList = []
    teamopr = calcTeamOpr()

    for team in teamopr:
        teamoprList.append([team,teamopr[team]])

    sortedTeamopr = SortListInList(teamoprList)

    for item in sortedTeamopr:
        print("%s: %s" % (item[0], item[1]))

main()
