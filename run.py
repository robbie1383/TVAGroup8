import pandas as pd
import itertools
from random import randrange
from VotingSchemes.Borda import BordaVoting
from VotingSchemes.PluralityVoting import PluralityVoting
from VotingSchemes.VotingForTwo import VotingForTwo
from VotingSchemes.AntiPluralityVoting import AntiPluralityVoting
from VotingSchemes.Sequential import Sequential


def happiness(voter: str, preferences, outcome: str, happinessMetric: int) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: a candidate that won some election
    :param happinessMetric: happiness function calculation scheme
    :return: happiness of one voter in the given scenario
    """
    preferencesVoter = preferences[voter].tolist()
    nrOutcomes = len(preferencesVoter)
    winnerRank = preferencesVoter.index(outcome)

    if winnerRank == 0:
        return 1
    if happinessMetric == 0:  # steep curve
        return 1 / (2 ** winnerRank)
    if happinessMetric == 1:  # linear curve
        return (nrOutcomes - winnerRank) / nrOutcomes
    if happinessMetric == 2:  # combined curve
        return (nrOutcomes - winnerRank) / (2 * nrOutcomes)


def overallHappiness(preferences, outcome: str, happinessMetric: int) -> float:
    """
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: a candidate that won some election
    :param happinessMetric: happiness function calculation scheme
    :return: overall happiness of all voters
    """
    sum = 0
    for voter in preferences.columns:
        sum += happiness(voter, preferences, outcome, happinessMetric)
    return sum


def strategicVoting(voter: str, preferences, votingScheme, happinessMetric: int):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :param happinessMetric: happiness function calculation scheme
    :return: a strategic voting option of the form :
             [newVoterRanking, outcome, trueHappiness, newHappiness, trueOverallHappiness, newOverallHappiness]
    """
    voterRanking = preferences[voter]
    permutations = list(itertools.permutations(list(voterRanking)))
    strategies = []
    for alternative in permutations:
        newPreferences = preferences.copy()
        newPreferences[voter] = alternative
        outcome = votingScheme.outcome(newPreferences)
        option = [alternative, outcome,
                  happiness(voter, preferences, outcome, happinessMetric),
                  happiness(voter, newPreferences, outcome, happinessMetric),
                  overallHappiness(preferences, outcome, happinessMetric),
                  overallHappiness(newPreferences, outcome, happinessMetric)]
        strategies.append(option)
    return strategies


def risk(voter: str, preferences, votingScheme, happinessMetric: int):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :param happinessMetric: happiness function calculation scheme
    :return:
    """
    manipulated = 0
    originalOutcome = votingScheme.outcome(preferences)
    originalHappiness = happiness(voter, preferences, originalOutcome, happinessMetric)
    originalOverallHappiness = overallHappiness(preferences, originalOutcome, happinessMetric)
    strategies = strategicVoting(voter, preferences, votingScheme, happinessMetric)
    for strategy in strategies:
        if (strategy[4] < originalOverallHappiness) & (strategy[2] > originalHappiness):
            manipulated += 1
    return manipulated / len(strategies)


def inputChecker(preferences):
    """
    :param preferences: pandas dataframe with the voting preferences
    :return: boolean value of whether the election is correct
    """
    n = len(preferences.index)
    options = [chr(ord("A") + i) for i in range(n)]
    for column in preferences.columns:
        if "Voter " not in column:
            print("\nColumn name <<", column,
                  ">> is not specified correctly. Use <<Voter n>> for the column names.\n")
            return False
        optionsCopy = options.copy()
        for element in preferences[column]:
            if pd.isnull(element):
                print("\nColumn name <<", column,
                      ">> contains an empty rating.\n")
                return False
            if element in optionsCopy:
                optionsCopy.remove(element)
            else:
                print("\nColumn name <<", column,
                      ">> contains two votes for candidate", element, ".\n")
                return False
    return True


def inputPreferences():
    """
    :return: pandas dataframe with the voting preferences
    """
    correct = False
    while not correct:
        print("This software uses .csv files as input. Please enter the name of your file as <name>.csv below.")
        print("If you wish to use the pre-defined example, press Enter.")
        inputFile = input(">> ")
        if len(inputFile) == 0:
            inputFile = "example.csv"
        preferences = pd.read_csv(inputFile)
        check = inputChecker(preferences)
        if check:
            correct = True
        else:
            print("Input file contains problems. Try again.")
    print("\nPreview of the file used:")
    print(preferences.head(5))
    return preferences


def inputVotingScheme():
    """
    :return: initialized voting scheme
    """
    votingOptions = [BordaVoting(), PluralityVoting(), AntiPluralityVoting(), VotingForTwo(), Sequential()]
    print("\nSelect one of the voting schemes below by entering its number id.")
    for scheme in range(len(votingOptions)):
        print(scheme, ":", votingOptions[scheme].toString())
    print("If you wish to use a random voting scheme, press Enter.")
    votingSchemeChoice = "start"
    while not (votingSchemeChoice in "01234" or len(votingSchemeChoice) == 0):
        votingSchemeChoice = input(">> ")

    if len(votingSchemeChoice) == 0:
        votingSchemeChoice = randrange(5)
    votingScheme = votingOptions[int(votingSchemeChoice)]
    print("\nVoting scheme selected is", votingScheme.toString())
    return votingScheme


def inputHappiness():
    """
    :return: int representing happiness curve
    """
    print("\nSelect what kind of happiness function you want to use by entering its number id.")
    print("0 : Steep curve happiness : ")
    print("1 : Linear curve happiness : ")
    print("2 : Combined curve happiness : ")
    print("If you wish to select a random curve, press Enter.")
    happinessChoice = "start"
    while not (happinessChoice in "012" or len(happinessChoice) == 0):
        happinessChoice = input(">> ")
    if len(happinessChoice) == 0:
        happinessChoice = randrange(3)
    happinessChoice = int(happinessChoice)
    if happinessChoice == 0:
        print("\nHappiness function selected uses a steep curve.")
    if happinessChoice == 1:
        print("\nHappiness function selected uses a linear curve.")
    if happinessChoice == 2:
        print("\nHappiness function selected uses a combined curve.")
    return happinessChoice


def createCommands(votingScheme):
    """
    :param votingScheme: initialized voting scheme
    :return: a string containing all option inputs
             a string containing the explanation of all commands
    """
    options = "help0123456"
    commands = "\nSelect one of the commands below by selecting its number id."
    commands += "\n0 : Quit the program."
    commands += "\n1 : Print the social ranking of this scenario."
    commands += "\n2 : Print the winner of this scenario."
    commands += "\n3 : Print the strategic voting options for some voter."
    commands += "\n4 : Print the happiness of some voter or all voters."
    commands += "\n5 : Print the overall happiness of this scenario."
    commands += "\n6 : Print the risk of strategic voting for some voter."
    if votingScheme.toString() == "Sequential Voting Scheme":
        options += "7"
        commands += "\n7 : Update the voting agenda."
    commands += "\nhelp : Prints a list of all the commands."

    return options, commands


def main():
    print("Welcome to the voting simulator.")

    # Set scenario parameters
    preferences = inputPreferences()
    votingScheme = inputVotingScheme()
    happinessChoice = inputHappiness()

    # Command loop
    options, commands = createCommands(votingScheme)
    print(commands)
    command = input("\n>> ")
    while command != "0":
        if command not in options:
            print("Command", command,
                  "is not supported. Use <help> for a list of commands.")

        if command == "help":
            print(commands)

        if command == "1":
            print("Social ranking of this scenario is :")
            print(votingScheme.outputScores(preferences))

        if command == "2":
            print("Winning candidate in this scenario is :")
            print(votingScheme.outcome(preferences))

        if command == "3":
            print("Enter the number id of the voter you want to use.")
            voter = input(">> ")
            voter = "Voter " + voter
            if voter not in preferences.columns:
                print("This voter does not exist.")
            else:
                print("The strategic voting options for this voter are :")
                print("newVoterRanking, newOutcome, trueHappiness, newHappiness, trueOverallHappiness, newOverallHappiness")
                strategies = strategicVoting(
                    voter, preferences, votingScheme, happinessChoice)
                for s in strategies:
                    print(s)

        if command == "4":
            print(
                "Enter the number id of the voter you want to use. Enter <all> to get a list of all.")
            voter = input(">> ")
            outcome = votingScheme.outcome(preferences)
            if voter == "all":
                h = []
                for v in preferences.columns:
                    h.append(happiness(v, preferences,
                             outcome, happinessChoice))
                print(preferences.columns.tolist())
                print(h)
            else:
                voter = "Voter " + voter
                if voter not in preferences.columns:
                    print("This voter does not exist.")
                else:
                    print("The happiness value for", voter, "is :")
                    print(happiness(voter, preferences, outcome, happinessChoice))

        if command == "5":
            print("The overall happiness in this scenario is :")
            outcome = votingScheme.outcome(preferences)
            print(overallHappiness(preferences, outcome, happinessChoice))

        if command == "6":
            print(
                "Enter the number id of the voter you want to use. Enter <all> to get a list of all.")
            voter = input(">> ")
            if voter == "all":
                h = []
                for v in preferences.columns:
                    h .append(
                        risk(v, preferences, votingScheme, happinessChoice))
                print(preferences.columns.tolist())
                print(h)
            else:
                voter = "Voter " + voter
                if voter not in preferences.columns:
                    print("This voter does not exist.")
                else:
                    print("The risk of strategic voting for", voter, "is :")
                    print(risk(voter, preferences, votingScheme, happinessChoice))

        if command == "7":
            if type(votingScheme) is Sequential:
                print("Enter the new agenda as <<A, B, C, D>>.")
                agenda = input(">> ")
                check = votingScheme.setAgenda(agenda.split(', '))
                if check:
                    print("Voting agenda set to:", votingScheme.agenda)
            else:
                print("Command", command,
                      "is not supported. Use <help> for a list of commands.")

        command = input("\n>> ")

    print("Simulation ended.")


if __name__ == "__main__":
    main()
