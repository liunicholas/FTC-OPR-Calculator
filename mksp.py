def getScores():
    infile = open("scores.txt", 'r')
    teams = []
    scores = []
    indTeams = []

    for line in infile:
        teamBreak = line.index("+")
        scoreBreak = line.index("=")

        team1 = line[:teamBreak]
        team2 = line[teamBreak+1:scoreBreak]
        score = line[scoreBreak+1:]

        teams.append([team1,team2])
        scores.append(score.strip())

        if team1 not in indTeams:
            indTeams.append(team1.strip())
        if team2 not in indTeams:
            indTeams.append(team2.strip())

    infile.close()

    return teams, scores, indTeams

def makeSympy(teams, scores, indTeams):
    outfile = open("mkspexec.txt", 'w')

    # outfile.write("from sympy import *\n")
    # outfile.write("def main():\n")

    teamSymsVars = ""
    for i in range(len(indTeams)):
        teamSymsVars += indTeams[i]
        if i != len(indTeams)-1:
            teamSymsVars += ", "

    teamSymsParams = ""
    for i in range(len(indTeams)):
        teamSymsParams += indTeams[i]
        if i != len(indTeams)-1:
            teamSymsParams += " "

    outfile.write("\t%s = symbols(\"%s\")\n" % (teamSymsVars, teamSymsParams))

    outfile.write("\tequations = [")
    for i in range(len(scores)):
        outfile.write("Eq(%s + %s, %d), " % (teams[i][0], teams[i][1], int(scores[i])+500))
    outfile.write("]\n")

    outfile.write("\n\tteamopr = solve(equations)")

    outfile.write("\n\treturn teamopr")

    # songFile.write("main()")

    outfile.close()

def main():
    teams, scores, indTeams = getScores()
    makeSympy(teams, scores, indTeams)

main()
