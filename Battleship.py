import random
import os

# *******************
# Prepare functions
# *******************


def preSet():
    mainList = []
    for i in range(_mapSize):
        tempList = []
        for j in range(_mapSize):
            tempList.append("( )")
        mainList.append(tempList)
    return mainList


def menu():
    clear()
    print("Hello {0}! Are you ready to go into battle?\nPlease choose an option:".format(_playerName))
    print("1, New Game")
    print("2, Shopping")
    print("3, Save Game")
    print("4, Load Game")
    print("5, Exit")

    selected = getchar()
    return selected


def determineStarter():
    playerStartValue = 0
    aiStartValue = 0
    while playerStartValue == aiStartValue:
        playerStartValue = random.randint(1, 10)
        aiStartValue = random.randint(1, 10)
    if aiStartValue < playerStartValue:
        return True
    else:
        return False


def setupShips(shipNo):
    error = 0
    ship = []
    shipInit = [4, 5]
    while True:
        clear()
        for y in range(_mapSize):
            for x in range(_mapSize):
                if shipInit[0] == y and shipInit[1] == x:
                    print("(X)", end="")
                else:
                    print(_field1[y][x], end="")
            print("\t\t\t", end="")
            print("\r")
        print(refreshReason(error))
        print("Choose starting point for this ship. It will be {0} field long.".format(_ships[shipNo]))
        print("Hit w, a, s, d to move start point, hit Enter to select space for the ship.")
        print("You can also it x to leave game.")
        error = 0
        direction = getchar()
        if direction in _moveInputs:
            shipInit = move(shipInit, direction)
            continue
        elif direction == "x":
            break
        elif direction == "\r":
            print("Now choose in which direction to extend it using w, a, s, d: ")
            extend = getchar()
            if extend in _moveInputs:
                if validateRange(shipInit, extend, shipNo, 1) is True:
                    if validateCross(shipInit, extend, shipNo, 1) is True:
                        ship = placeShip(shipInit, extend, shipNo, 1)
                        return ship
                    else:
                        error = 2
                        continue
                else:
                    error = 1
                continue


def aiSetupShips(j):
    while True:
        shipZero = []
        shipZero.append(random.randint(0, 9))
        shipZero.append(random.randint(0, 9))
        if _field2[shipZero[0]][shipZero[1]] == _liveShip:
            continue
        else:
            randDir = _moveInputs[random.randint(0, 3)]
            if validateRange(shipZero, randDir, j, 2) is True:
                if validateCross(shipZero, randDir, j, 2) is True:
                    return placeShip(shipZero, randDir, j, 2)


def placeShip(startCoor, direction, ship, player):
    shipCoords = []
    if player == 1:
        workField = _field1
    else:
        workField = _field2

    if direction == "w":
        for i in range(_ships[ship]):
            workField[startCoor[0] - i][startCoor[1]] = _liveShip
            shipCoords.append([startCoor[0] - i, startCoor[1]])
    elif direction == "s":
        for i in range(_ships[ship]):
            workField[startCoor[0] + i][startCoor[1]] = _liveShip
            shipCoords.append([startCoor[0] + i, startCoor[1]])
    elif direction == "a":
        for i in range(_ships[ship]):
            workField[startCoor[0]][startCoor[1] - i] = _liveShip
            shipCoords.append([startCoor[0], startCoor[1] - i])
    elif direction == "d":
        for i in range(_ships[ship]):
            workField[startCoor[0]][startCoor[1] + i] = _liveShip
            shipCoords.append([startCoor[0], startCoor[1] + i])
    return shipCoords


def validateCross(startCoor, direction, ship, player):
    fields = []
    if player == 1:
        fieldToCheck = _field1
    else:
        fieldToCheck = _field2
    for i in range(-1, _ships[ship] + 1):
        for j in range(-1, 2):
            if direction == "w":
                if startCoor[0] - i >= _mapSize or startCoor[1] + j >= _mapSize or startCoor[0] - i < 0 or startCoor[1] + j < 0:
                    continue
                else:
                    fields.append(fieldToCheck[startCoor[0] - i][startCoor[1] + j])
            if direction == "s":
                if startCoor[0] + i >= _mapSize or startCoor[1] + j >= _mapSize or startCoor[0] + i < 0 or startCoor[1] + j < 0:
                    continue
                else:
                    fields.append(fieldToCheck[startCoor[0] + i][startCoor[1] + j])
            if direction == "a":
                if startCoor[0] + j >= _mapSize or startCoor[1] - i >= _mapSize or startCoor[0] + j < 0 or startCoor[1] - i < 0:
                    continue
                else:
                    fields.append(fieldToCheck[startCoor[0] + j][startCoor[1] - i])
            if direction == "d":
                if startCoor[0] + j >= _mapSize or startCoor[1] + i >= _mapSize or startCoor[0] + j < 0 or startCoor[1] + i < 0:
                    continue
                else:
                    fields.append(fieldToCheck[startCoor[0] + j][startCoor[1] + i])
    if _liveShip in fields:
        return False
    else:
        return True


# ***************
# Sys functions
# ***************


def screen(gameState, coor=[20, 20]):
    y = 0
    while(y < _mapSize):
        for x in range(_mapSize):
            print(_field1[y][x], end="")
        print("\t\t\t", end="")
        for x in range(_mapSize):
            if y == coor[0] and x == coor[1]:
                print("(X)", end="")
            elif _field2[y][x] == _liveShip and _gameState == 1:
                print("( )", end="")
            else:
                print(_field2[y][x], end="")
        print("\r")
        y += 1


def refreshReason(errorNo):
    if errorNo == 0:
        return ""
    elif errorNo == 1:
        return "Your ship is too large, or the land is too strong. Try again!"
    elif errorNo == 2:
        return "Ships would be too close to eachother. Try again!"
    elif errorNo == 3:
        return "You have shoot there already!"


def getchar():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def clear():
    os.system('clear')


# ******************
# In-Game functions
# ******************


def move(startCoor, direction):
    backup = list(startCoor)
    if direction == "w":
        startCoor[0] -= 1
    elif direction == "s":
        startCoor[0] += 1
    elif direction == "a":
        startCoor[1] -= 1
    else:
        startCoor[1] += 1

    if min(startCoor) < 0 or max(startCoor) >= _mapSize:
        return backup
    else:
        return startCoor


def validateRange(startCoor, direction, ship, player):
    toCheck = list(startCoor)
    if player == 1:
        shipLength = _ships[ship]
    else:
        shipLength = _aiShips[ship]

    if direction == "w":
        toCheck[0] -= shipLength
    elif direction == "s":
        toCheck[0] += shipLength
    elif direction == "a":
        toCheck[1] -= shipLength
    elif direction == "d":
        toCheck[1] += shipLength

    if min(toCheck) < 0 or max(toCheck) >= _mapSize:
        return False
    else:
        return True


def guess():
    targetCoor = [4, 5]
    error = 0
    while True:
        clear()
        screen(_gameState, targetCoor)
        print(refreshReason(error))
        error = 0
        print("Choose target field and it Enter to fire!")
        direction = getchar()
        if direction in _moveInputs:
            targetCoor = move(targetCoor, direction)
            continue
        elif direction == "\r":
            if fire(targetCoor) == 1:
                _field2[targetCoor[0]][targetCoor[1]] = _woundedShip
                return
            elif fire(targetCoor) == 2:
                _field2[targetCoor[0]][targetCoor[1]] = _missed
                return
            elif fire(targetCoor) == 3:
                error = 3
                continue


def aiGuess():
    x = 0
    y = 0
    targetCoor = []
    for y in range(len(_field1)):
        for x in range(len(_field1[y])):
            if _field1[y][x] == _woundedShip:
                targetCoor = woundedTarget(y, x)
                hit = fire(targetCoor)
                if hit == 1:
                    _field1[targetCoor[0]][targetCoor[1]] = _woundedShip
                    return
                elif hit == 2:
                    _field1[targetCoor[0]][targetCoor[1]] = _missed
                    return

    while True:
        targetCoor = [random.randint(0, 9), random.randint(0, 9)]
        if _field1[targetCoor[0]][targetCoor[1]] in [_woundedShip, _deadShip, _missed]:
            continue
        else:
            if fire(targetCoor) == 1:
                _field1[targetCoor[0]][targetCoor[1]] = _woundedShip
                return
            elif fire(targetCoor) == 2:
                _field1[targetCoor[0]][targetCoor[1]] = _missed
                return


def woundedTarget(y, x):
    possibleTargets = []
    if _field1[y][x + 1] != _woundedShip and _field1[y + 1][x] != _woundedShip:
        possibleTargets.append([y - 1, x])
        possibleTargets.append([y + 1, x])
        possibleTargets.append([y, x - 1])
        possibleTargets.append([y, x + 1])

    elif _field1[y][x + 1] == _woundedShip:
        if _field1[y][x + 2] == _woundedShip:
            possibleTargets.append([y, x + 3])
        else:
            possibleTargets.append([y, x + 2])
        possibleTargets.append([y, x - 1])

    if _field1[y + 1][x] == _woundedShip:
        if _field1[y + 2][x] == _woundedShip:
            possibleTargets.append([y + 3, x])
        else:
            possibleTargets.append([y + 2, x])
        possibleTargets.append([y - 1, x])

    tempTargets = possibleTargets

    for coor in possibleTargets:
        if _field1[coor[0]][coor[1]] == _missed or min(coor) < 0 or max(coor) > 9:
            tempTargets.remove(coor)
    possibleTargets = tempTargets

    return possibleTargets[random.randint(0, len(possibleTargets)-1)]


def fire(targetCoor, weapon=1):

    if _activePlayer is True:
        fieldToCheck = _field2
    else:
        fieldToCheck = _field1

    if weapon == 1:
        if fieldToCheck[targetCoor[0]][targetCoor[1]] == _liveShip:
            return 1
        elif fieldToCheck[targetCoor[0]][targetCoor[1]] == "( )":
            return 2
        elif fieldToCheck[targetCoor[0]][targetCoor[1]] in [_missed, _woundedShip, _deadShip]:
            return 3


def checkDamage():
    if _activePlayer is True:
        shipsToCheck = _aiShipCoords
        fieldToCheck = _field2
    else:
        shipsToCheck = _shipCoords
        fieldToCheck = _field1
    print(shipsToCheck)

    for ship in shipsToCheck:
        stillAlive = []
        for coor in ship:
            if fieldToCheck[coor[0]][coor[1]] == _woundedShip:
                stillAlive.append(False)
            else:
                stillAlive.append(True)
        if True not in stillAlive:
            for coor in ship:
                fieldToCheck[coor[0]][coor[1]] = _deadShip
            return ship
    return "None"


def checkWin():
    x = 0
    if _activePlayer is True:
        fieldToCheck = _field2
    else:
        fieldToCheck = _field1

    for x in range(len(fieldToCheck)):
        if _liveShip in fieldToCheck[x] or _woundedShip in fieldToCheck[x]:
            return False
    return True


# **********
# ** Main **
# **********


clear()
_playerName = input("Please provide your name: ")
_ships = [2, 3, 4]
_aiShips = [2, 3, 4]
_shipCoords = []
_aiShipCoords = []
_moveInputs = ["w", "a", "s", "d"]
_liveShip = "(O)"
_woundedShip = "(@)"
_deadShip = "(Ø)"
_missed = "(-)"

while True:

    _gameState = 1
    _mapSize = 10
    _field1 = preSet()
    _field2 = preSet()
    i, j = 0, 0

    optionSelect = menu()
    if optionSelect == "5":
        break
    elif optionSelect == "4":
        continue
    elif optionSelect == "3":
        continue
    elif optionSelect == "2":
        continue
    elif optionSelect == "1":
        pass
    else:
        continue

    _activePlayer = determineStarter()
    while i < len(_ships):
        _shipCoords.append(setupShips(i))
        i += 1
    while j < len(_ships):
        _aiShipCoords.append(aiSetupShips(j))
        j += 1

    while _gameState == 1:

        clear()
        screen(_gameState)

        if _activePlayer is True:
            guess()
        else:
            aiGuess()

        sunken = checkDamage()
        if sunken != "None":
            if _activePlayer is True:
                _aiShipCoords.remove(sunken)
            else:
                _shipCoords.remove(sunken)

        if checkWin() is True:
            _gameState = 2
            break
        _activePlayer = not _activePlayer
