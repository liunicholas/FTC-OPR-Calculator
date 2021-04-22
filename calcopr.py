from os.path import isfile

def getUserFile():
    while True:
        userFile = raw_input("data file: ")
        if isfile(userFile):
            return userFile
        print("not found\n")

def getScores(dataFile):
    infile = open(dataFile, 'r')
    matches = []
    scores = []
    teamOPR = {}
    teamApps = {}
    teamNames = {}

    for line in infile:
        if line.strip() != "STOP":
            if line[0] == "#":
                split = line.index(":")
                name = line[split+1:].strip()
                name += (40) * " "
                teamNames[line[1:split]] = name
                continue

            teamBreak = line.index("+")
            scoreBreak = line.index("=")

            team1 = line[:teamBreak]
            team2 = line[teamBreak+1:scoreBreak]
            score = line[scoreBreak+1:]

            matches.append([team1,team2])
            scores.append(score.strip())

            if team1 not in teamApps:
                teamOPR[team1] = 0.0
                teamApps[team1] = 1
            else:
                teamApps[team1] += 1

            if team2 not in teamApps:
                teamOPR[team2] = 0.0
                teamApps[team2] = 1
            else:
                teamApps[team2] += 1

        else:
            infile.close()
            return matches, scores, teamOPR, teamApps, teamNames

    infile.close()
    return matches, scores, teamOPR, teamApps, teamNames

def getScoresOL(dataFile):
    infile = open(dataFile, 'r')
    matches = []
    scores = []
    teamOPR = {}
    teamApps = {}
    teamNames = {}

    for line in infile:
        if line[0] == "#":
            split = line.index(":")
            name = line[split+1:].strip()
            name += (40) * " "
            teamNames[line[1:split]] = name
            continue

        checkVal = False
        checkSpace = True
        sil = []
        for i in range(len(line)):
            if checkSpace:
                if line[i] == " " or line[i] == "\t":
                    sil.append(i)
                    checkSpace = False
                    checkVal = True
            if checkVal:
                if line[i] != " ":
                    checkSpace = True
                    checkVal = False

        team1 = line[sil[2]+1:sil[3]].strip()
        team2 = line[sil[3]+1:sil[4]].strip()
        team3 = line[sil[4]+1:sil[5]].strip()
        team4 = line[sil[5]+1:sil[6]].strip()
        score1 = line[sil[6]+1:sil[7]].strip()
        score2 = line[sil[7]:].strip()

        matches.append([team1,team2])
        scores.append(score1)

        matches.append([team3,team4])
        scores.append(score2)

        if team1 not in teamApps:
            teamOPR[team1] = 0.0
            teamApps[team1] = 1
        else:
            teamApps[team1] += 1

        if team2 not in teamApps:
            teamOPR[team2] = 0.0
            teamApps[team2] = 1
        else:
            teamApps[team2] += 1

        if team3 not in teamApps:
            teamOPR[team3] = 0.0
            teamApps[team3] = 1
        else:
            teamApps[team3] += 1

        if team4 not in teamApps:
            teamOPR[team4] = 0.0
            teamApps[team4] = 1
        else:
            teamApps[team4] += 1

    infile.close()

    return matches, scores, teamOPR, teamApps, teamNames

def initialCalculation(matches, scores, teamOPR, teamApps):
    for i in range(len(matches)):
        team1 = matches[i][0]
        team2 = matches[i][1]
        score = int(scores[i])

        teamOPR[team1] += score/2
        teamOPR[team2] += score/2

    for team in teamOPR:
        teamOPR[team] /= teamApps[team]

    return teamOPR

def loopAdjustOPR(matches, scores, teamOPR, teamApps, loops):
    for n in range(loops):
        newTeamOPR = {}
        for team in teamOPR:
            newTeamOPR[team] = 0

        for i in range(len(matches)):
            team1 = matches[i][0]
            team2 = matches[i][1]
            score = float(scores[i])

            frac1 = teamOPR[team1] / (teamOPR[team1]+teamOPR[team2])
            frac2 = teamOPR[team2] / (teamOPR[team1]+teamOPR[team2])

            newTeamOPR[team1] += score * frac1
            newTeamOPR[team2] += score * frac2

        for team in newTeamOPR:
            newTeamOPR[team] /= teamApps[team]

        teamOPR = newTeamOPR

    return teamOPR

def displayData(teamOPR, teamNames):
    sortedData = sorted(teamOPR, key=teamOPR.__getitem__)
    print("\n%s %17s %10s"  % ("Team:", "#:", "OPR:"))
    for i in range(len(sortedData)-1,-1,-1):
        print("%.20s %0.5s    %.2f" % (teamNames[sortedData[i]], str(sortedData[i]) + " " * 5, teamOPR[sortedData[i]]))
    print("")

def main():
    dataFile = getUserFile()

    matches, scores, teamOPR, teamApps, teamNames = getScores(dataFile)

    teamOPR = initialCalculation(matches, scores, teamOPR, teamApps)

    teamOPR = loopAdjustOPR(matches, scores, teamOPR, teamApps, 100)
    displayData(teamOPR, teamNames)

main()
