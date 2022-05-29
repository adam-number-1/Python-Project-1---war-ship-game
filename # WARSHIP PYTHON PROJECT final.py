# WARSHIP PYTHON PROJECT
# this is my own project of a warship human against ai.
# player inputs his name, player gets to choose, where to put his ships, then ai puts his ships too 
# then a program randomly chooses starting player
# then the game takes places step by step while printing the game grid with every step
# once someone´s ships get fully destroyed, the program gives a choice to play again or quit

from msilib import add_stream
import random
import time
# AI class
# player class - creates player objects
class Player:
    def __init__(self, name, lives):
        self.name=name
        self.lives=lives
        self.ship_list = []
        #dictionary of ship coordinates and their numbers for printing into the game map
        self.ship_dictionary = {}
        #dictionary of players chosen strikes with the value either X as miss, H as hit and S as sunk ship
        self.strike_dictionary={}
        self.strike_options = set()

# separate class just for ai foolow up shots decision process
class AI:
    def __init__(self):
        # sink mode means when the AI is in mode of trying to finish already hit ship
        self.sink_mode = False
        # list of consecutive hits on a non-sunk ship
        self.follow_up_hits = []
        # just an attribute to decide, where the ai finds the hit ship being placed vertically or horizontally
        self.criteria = ""

    # if the AI hits human ship, it needs to calculate, where are the nearby options for follow up hit
    def follow_up_targets(self):
        print("AI is thinking")
        res=set()
        columns = "ABCDEFGHIJ"
        opt_columns_list = []
        opt_row_list = []

        # check how many hits of one ship were made before checking for follow up targets
        # the method is checking for this
        #            X
        #           XHX   - H is the hit coordinate of human ship
        #            X    - X is the follow up target
        # the method also removes from the suggestions, what is out of map.
        if len(self.follow_up_hits) == 1:
            #surronding columns
            if self.follow_up_hits[0][0] == "A":
                opt_columns_list.append("A")
                opt_columns_list.append("B")
            elif self.follow_up_hits[0][0] == "J":
                opt_columns_list.append("I")
                opt_columns_list.append("J")
            else:
                opt_columns_list.append(columns[columns.index(self.follow_up_hits[0][0])-1])
                opt_columns_list.append(self.follow_up_hits[0][0])
                opt_columns_list.append(columns[columns.index(self.follow_up_hits[0][0])+1])
            #surrounding rows
            if self.follow_up_hits[0][1:] == "1":
                opt_row_list.append("1")
                opt_row_list.append("2")
            elif self.follow_up_hits[0][1:] == "10":
                opt_row_list.append("9")
                opt_row_list.append("10")
            else:
                opt_row_list.append(str(int(self.follow_up_hits[0][1:])-1))
                opt_row_list.append(self.follow_up_hits[0][1:])
                opt_row_list.append(str(int(self.follow_up_hits[0][1:])+1))
            # add follow up targets while removing diagonal options
            for i in opt_columns_list:
                for j in opt_row_list:
                    if i == self.follow_up_hits[0][0] or j == self.follow_up_hits[0][1:]:
                        res.add(i+j)
        elif len(self.follow_up_hits) == 2:
            # find out if the hits are horizontal or vertical
            if self.follow_up_hits[0][0] == self.follow_up_hits[1][0]:
                self.criteria = "vertical"
                #sort them by the row number - canť do it alphabetically, because then "10" < "9"
                if int(self.follow_up_hits[0][1:]) > int(self.follow_up_hits[1][1:]):
                    a = self.follow_up_hits[0]
                    b = self.follow_up_hits[1]
                    self.follow_up_hits[1] = a
                    self.follow_up_hits[0] = b  
                # add to the targets options right above and under these two hits while checking, if the option is withing the game table
                if self.follow_up_hits[0][1:]!="1":
                    res.add(self.follow_up_hits[0][0] + str(int(self.follow_up_hits[0][1:])-1))
                if self.follow_up_hits[1][1:]!="10":
                    res.add(self.follow_up_hits[1][0] + str(int(self.follow_up_hits[1][1:])+1))
            else:
                self.criteria = "horizontal"
                #sort them by the column  
                if self.follow_up_hits[0][0] > self.follow_up_hits[1][0]:
                    a = self.follow_up_hits[0]
                    b = self.follow_up_hits[1]
                    self.follow_up_hits[1] = a
                    self.follow_up_hits[0] = b    
                # add to the targets options right on the left and right to these two hits while checking, if the option is withing the game table
                if self.follow_up_hits[0][0]!="A":
                    res.add(columns[columns.index(self.follow_up_hits[0][0])-1] + self.follow_up_hits[0][1:])
                if self.follow_up_hits[1][0]!="J":
                    res.add(columns[columns.index(self.follow_up_hits[1][0])+1] + self.follow_up_hits[1][1:])    
        # there is more than 2 - again I have to add options vertically or horizontally, while adding the new hit either
        # on the beginning of the hit list or the end of it and repeating the same as if there were two hits     
        else:
            if self.criteria == "vertical":
            # if the ai makes a hit, the program will append this new hit position on the end of the hit list
            # need to check, if it belong to the end of it and if not, move it to the beginning
                if int(self.follow_up_hits [-1][1:]) < int(self.follow_up_hits [0][1:]):
                    temp_list = []
                    temp_list.append(self.follow_up_hits[-1])
                    for i in range(len(self.follow_up_hits)-1):
                        temp_list.append(self.follow_up_hits[i])
                    self.follow_up_hits = temp_list

               # add to the targets options right above and under these two hits while checking, if the option is withing the game table
                if self.follow_up_hits[0][1:]!="1":
                    res.add(self.follow_up_hits[0][0] + str(int(self.follow_up_hits[0][1:])-1))
                if self.follow_up_hits[-1][1:]!="10":
                    res.add(self.follow_up_hits[-1][0] + str(int(self.follow_up_hits[-1][1:])+1))
            else:
                if self.follow_up_hits[0][0] > self.follow_up_hits[-1][0]:
                    temp_list = []
                    temp_list.append(self.follow_up_hits[-1])
                    for i in range(len(self.follow_up_hits)-1):
                        temp_list.append(self.follow_up_hits[i])
                    self.follow_up_hits = temp_list

                    
                # add to the targets options right on the left and right to these two hits while checking, if the option is withing the game table
                if self.follow_up_hits[0][0]!="A":
                    res.add(columns[columns.index(self.follow_up_hits[0][0])-1] + self.follow_up_hits[0][1:])
                if self.follow_up_hits[-1][0]!="J":
                    res.add(columns[columns.index(self.follow_up_hits[-1][0])+1] + self.follow_up_hits[-1][1:])  
        print("AI knows, where to hit next")                  
        return res


# class - creates initial table object and display
class Progress_table:
    def __init__(self):
        # display dictionary asigns indexes of a display list to each coordinate, co it is easier to change the shape of the game map
        self.display_dictionary = {}
        
        for i in range(0,10):
            for j in range(1,11):
                self.display_dictionary["ABCDEFGHIJ"[i]+str(j)]= (j,i+1)

        # this just gives an option to change the initial value in the empty table. default is "."    
        self.initial_value_dictionary= {}
        for i in "ABCDEFGHIJ":
            for j in range(1,11):
                self.initial_value_dictionary[i+str(j)]= "."
    # the table is accessed as property an the reason for that is I want to layer the base table, the ships and hit on top of each
    # other. I do not want to modify the initial table, so it is easier to always display different things
    @property
    def table(self):
        return [["  ","A","B","C","D","E","F","G","H","I","J"],
        [" 1",".",".",".",".",".",".",".",".",".","."],
        [" 2",".",".",".",".",".",".",".",".",".","."],
        [" 3",".",".",".",".",".",".",".",".",".","."],
        [" 4",".",".",".",".",".",".",".",".",".","."],
        [" 5",".",".",".",".",".",".",".",".",".","."],
        [" 6",".",".",".",".",".",".",".",".",".","."],
        [" 7",".",".",".",".",".",".",".",".",".","."],
        [" 8",".",".",".",".",".",".",".",".",".","."],
        [" 9",".",".",".",".",".",".",".",".",".","."],
        ["10",".",".",".",".",".",".",".",".",".","."]]

    # this just takes the whole game table or map and prints it out
    def print_game_progress(a,b):
        for i in range(len(a)):
            print(a[i]+b[i])

    # this is a static method for displaying coordinates, which are used just once and don´t initially come as a dictionary
    # like a set of follow up options, when placing a ship for example
    @staticmethod
    def set_to_dictionary(block_set, display_value):
        display_values = {}
        for i in block_set:
            display_values[i]=display_value
        return display_values

    # this is where the final game table for printing is made. It takes the initial value dictionary and updates it with whatever is passed
    # by the program to be printed
    def table_to_print(self,*dict):

        full_dictionary={}
        full_dictionary.update(self.initial_value_dictionary)

        
        for i in dict:
            full_dictionary.update(i)

        res_table=self.table

        for i in full_dictionary:
            table_position = self.display_dictionary[i]
            res_table[table_position[0]][table_position[1]] = full_dictionary[i]
        return res_table
        
# class for ship placement methods
class Ship_placement:
    def __init__(self):
        # initial options, where a ship can be placed
        self.options=set()
        for i in 'ABCDEFGHIJ':
            for j in range(1,11):
                self.options.add(i+str(j))

    # this method calculates the follow up options
    # it takes the first coordinate of the ship and calculates from the available options, where can be
    # the ending point of the ship while not allowing to add options, which are out of the game map
    def follow_up_options(previous, ship_length):
        temp=[]
        column_index = "ABCDEFGHIJ".index(previous[0])  
        row_index = int(previous[1:])
        # up, down, left, right options
        temp = [[column_index,row_index - ship_length + 1],
                [column_index,row_index + ship_length - 1],
                [column_index - ship_length + 1,row_index],
                [column_index + ship_length - 1,row_index]]
        temp2=set()
        for i in range(4):
            if (temp[i][0] > -1 and temp[i][0] < 10) and (temp[i][1] > 0 and temp[i][1] < 11):
                temp2.add( "ABCDEFGHIJ"[temp[i][0]] + str(temp[i][1]))
        
        return temp2

    # once there is a begiining point and ending point of a ship, this method creates the rest of the coordinates of the ship
    def ship_coordinates(beginning, end):
        coordinates = set()
        # ship oriented from up to down in the same column
        if beginning[0] == end[0] and int(beginning[1:]) < int(end[1:]):
            for i in range(int(beginning[1:]),int(end[1:])+1):
                coordinates.add(beginning[0]+str(i))
        # ship oriented from down to up in the same column
        if beginning[0] == end[0] and int(beginning[1:]) > int(end[1:]):
            for i in range(int(beginning[1:]),int(end[1:])-1, -1):
                coordinates.add(beginning[0]+str(i))
        # ship oriented from left to right in same row
        if beginning[0] < end[0] and beginning[1:] == end[1:]:
            for i in "ABCDEFGHIJ"[("ABCDEFGHIJ").index(beginning[0]):("ABCDEFGHIJ").index(end[0])+1]:
                coordinates.add(i+beginning[1:])
        # ship oriented from left to right in same row
        if beginning[0] > end[0] and beginning[1:] == end[1:]:
            for i in "ABCDEFGHIJ"[("ABCDEFGHIJ").index(end[0]):("ABCDEFGHIJ").index(beginning[0])+1]:
                coordinates.add(i+beginning[1:])
        return coordinates

    # one of the rules of the game is, that ships can!t share borders. To ensure that, every time a ship is created,
    # this method calculates its boundaries, so these coordinates can be removed from the options
    # example:     XXXXX
    #              X333X
    #              XXXXX where X is the boundary position
    def ship_boundary(ship_cord):
        row = "123456789"
        column = "ABCDEFGHIJ"
        boundary=set()
        for i in list(ship_cord):  
            if i[0] == "A":
                temp_boundary_column=["A","B"]
            elif i[0] == "J":
                temp_boundary_column=["I","J"]
            else:
                temp_boundary_column=[column[column.index(i[0])-1], i[0],column[column.index(i[0])+1]]
            
            if i[1:] == "1":
                temp_boundary_row = ["1","2"]
            elif i[1:] == "10":
                temp_boundary_row = ["9","10"]
            elif i[1:] == "9":
                temp_boundary_row = ["8","9","10"]
            else:
                temp_boundary_row=[row[row.index(i[1])-1], i[1],row[row.index(i[1])+1]]
            for j in temp_boundary_column:
                for k in temp_boundary_row:
                    boundary.add(j+k)
        boundary= boundary.difference(ship_cord)
        return boundary


# ship class - creates ship objects
class Ship:
    # dictionary for this class, so I can put in the constructor less parameters
    type_dict = {
        "carrier":5,
        "battleship":4,
        "cruiser":3,
        "submarine":3,
        "destroyer":2
    }
    def __init__(self,coordinates,type):
        self.coordinates = coordinates
        self.type=type
        self.lives = Ship.type_dict[type]

def start_game():

    print_decor(print_decor(print))('WELCOME TO THE WARSHIP: HUMAN vs. AI')
    print('It is a classic warship game, each player has 5 ships')
    print('Carrier - 5 blocks, Battleship - 4 blocks, Cruiser - 3 blocks, Submarine - 3 blocks and Destroyer - 2 blocks')
    print('The game start by human player choosing his name followed by human placing ships on the map')
    print('The ships on the map cannot cross each other or share either corner or any side')
    print('The map is a 10 by 10 grid from A1 to J10')
    print('After the human player is done with placing the ships, the AI places its ships as well')
    print('Once AI is done, program randomly chooses the starting player')
    print('First player chooses, where to strike on the opponents map. If the player hits the target, they repeat their turn')
    print('If the player misses the target, it is the opponents turn and so on, until all of the ships of somme of the players are destroyed')

# decorator method for printing important messages
def print_decor(f):
    def wrap(text):

        print('====================================')
        f(text)
        print('====================================')

    return wrap

# the player turn method - this is where the players choose strikes and where the main part of the game happens
def player_turn(player):

    # the turns for human and ai differ very little. I made it in one method.
    if player != ai:
        opponent = ai
        while True: 
            try:
                # input human strike choice
                strike = input(player.name + ", choose where to strike: ")
                strike = strike[0].upper() + strike[1:]
                # remove the strike choice from the list of strike positions - this will throw error, if human made invalid input
                player.strike_options.remove(strike)
                print("You have chosen: "+strike)
                time.sleep(1)
                break
            except:
                print(strike +" is not a valid strike option. Try again: ")
                continue
    else:
        opponent = human
        print("AI chooses, where to strike.")
        time.sleep(2)
        # here the program checks, if the AI isn´t trying to finish a damaged opponent ship
        # if yes, the AI will not make a random choice from all options, but only from suggested options
        if AI_object.sink_mode == True:
            print("AI is figuring out the follow up strike options...")
            time.sleep(1)
            sink_options = AI_object.follow_up_targets().intersection(player.strike_options)
            time.sleep(1)
            print(sink_options)
            strike = random.choice(list(sink_options))

        else:
            strike = random.choice(list(player.strike_options))
        

        time.sleep(1)
        print("AI has chosen: " +strike)
        time.sleep(1)
        player.strike_options.remove(strike)

    # the progrm checks if the selected coordinate is in opponents ship dictionary
    if strike in opponent.ship_dictionary.keys():
        # decrease opponent lives by 1 (obviously with fixed amount of ships, there is fixed amount of hits, easy victory condition)
        opponent.lives -= 1 
        # find the corresponding opponent ship
        for i in opponent.ship_list:
            if strike in i.coordinates:
                i.lives -=1
                # if the ship doesn´t have any lives left, it is marked as sunk
                if i.lives < 1:
                    for j in i.coordinates:
                       # turn all ship positions to SUNK
                       player.strike_dictionary[j]="S"
                    if player != ai:
                        print_decor(print_decor(print))(player.name + ", you have destroyed AI\'s " + i.type +"!")
                        
                    else:
                        
                        print_decor(print_decor(print))("AI has destroyed your" + i.type +"!")
                        # the ai fully destroyed human ship, so the sink mode - that is what i call the mode, where ai is trying
                        # to finish damaged human ship, is turned off
                        AI_object.sink_mode = False
                        AI_object.follow_up_hits=[]
                        # ai understand, that if a ship was sunk, no other ship will have its part in the sunk ships's boundaries
                        # that is why it will remove this boundary from the strike options
                        sunk_ship_boundaries = Ship_placement.ship_boundary(i.coordinates)
                        print(sunk_ship_boundaries)
                        for k in sunk_ship_boundaries:
                            if k in player.strike_options:
                                player.strike_options.remove(k)    
                          
                       
                else:
                # put into list the hit coordinate with letter H as hit
                    player.strike_dictionary[strike]="H"
                    if player !=ai:
                        print_decor(print)(player.name + ", you have AI\'s ship!") 
                         
                    else:
                        print_decor(print)(player.name + " has hit your "+ i.type+"!")
                        # if ai made a first hit on human ship, it will try to finish the ship fully
                        AI_object.sink_mode = True
                        AI_object.follow_up_hits.append(strike) 
                break

        # the reason, why this method returns a player object after a turn is done is because
        # I don´t want to call this method again and draining memory
        return player
  
    else:
        print(player.name +", missed....")
        
        # coordinates of the miss goes into disctionary together with letter X
        player.strike_dictionary[strike]="X"


        return opponent


# this is the game method of players putting ships on places
def place_ships(player):
    
    ships_to_place = {
        "carrier" : "5",
        "battleship" : "4",
        "cruiser" : "3",
        "submarine" : "3",
        "destroyer" : "2",
    }

    # create list of free placement options for player
    player_options= Ship_placement().options 
    ship_boundaries = {}

    for i in ships_to_place:
    # infinite loop for player input
        if player != ai:
            while True:       
                try:
                    # input of first point of a ship by the the player
                    first_point = input('Choose the first coordinate of the '+i+' ship: ')
                    # converts first letter of the user input to upper
                    first_point = first_point[0].upper() + first_point[1:]
                    # remove first option from the list of free options
                    # this will cause error, if the player enters something wrong
                    player_options.remove(first_point)
                    break
                except:
                    print(first_point+" is not an available option. Try again: ")
                    continue
        else:
            first_point = random.choice(list(player_options))
            print("first_point for" + i )
            print(first_point)

            player_options.remove(first_point)      
        # the first point of player ship intentionally goes to dictionary, together with number of blocks of a ship
        # so errors can be thrown, if the program will try put duplicate the key value - like adding same coordinate twice
        d={first_point: ships_to_place[i]}

        # the program find out, where can an ending point of a ship be placed based on players first point selection
        second_point_options = Ship_placement.follow_up_options(first_point,int(ships_to_place[i]))

    
        #  this prints the updated game table with players first selection and follow up options
        # the follow up options are cleared from what is no longer available
        second_point_options = second_point_options.intersection(player_options)
        if player != ai:
            
            updated_player_table=human_table.table_to_print(d,Progress_table.set_to_dictionary(second_point_options,"O"))
            Progress_table.print_game_progress(updated_player_table, ai_table.table)
        

     
        if player != ai:
            # another human input while loop
            while True:
                print("Choose some of the options below for the second point of the ship: ")
                print(second_point_options)
                try:
                    second_point= input("Which of the options will be the second end of your ship?: ")
                    second_point = second_point[0].upper() + second_point[1:]
                    if second_point not in second_point_options:
                        raise
                    break 
                except:
                    print(second_point+" is not a follow-up options. Try again: ")
                    continue
        else:
                    print("second point options for"+ i)
                    print(second_point_options)
                    try: #in rare cases the ai chooses point in such a spot, that it is unable to finish the ship
                        second_point= random.choice(list(second_point_options))
                    except:
                        # in that case the program will call this method again for the AI player
                        player.ship_list = []
                        player.ship_dictionary = {}
                        place_ships(player)
                    print(second_point)

        
        d[second_point] = ships_to_place[i]

        # here the beginning and ending points of a ship are taken
        # the program calculates the remaining parts of the ship
        new_ship_position = Ship_placement.ship_coordinates(first_point, second_point)

        # since the ships can´t touch, cross or share a corner, program will take out the ship boundary from
        # the placement options
        for boundary in Ship_placement.ship_boundary(new_ship_position):
            ship_boundaries.update({boundary : "X"})   

        # for the removal a for loop is used, because trying to remove something from a set, which isn´t there causes error
        for j in ship_boundaries:
            if j in player_options:
                player_options.remove(j)

        # putting coordinatesand ship labels in each of the ship¨s dictionary
        #                   A B C D E
        # example:      1   5 5 5 5 5       {A1:5, ...}
        #
        for k in new_ship_position:
            player.ship_dictionary[k]=ships_to_place[i]
            if k in player_options:
                player_options.remove(k)
           
        # prints the table for human, so they can observe the progress of putting ships
        if player != ai:
            updated_player_table=human_table.table_to_print(human.ship_dictionary, ship_boundaries)
            Progress_table.print_game_progress(updated_player_table, ai_table.table)

        player.ship_list.append(Ship(new_ship_position, i))

#       ####### ###### #   # ######
###     #       #    # ## ## #
#####   #  #### ###### # # # ####
###     #     # #    # #   # #
#       ####### #    # #   # ######
while True:
    
    start_game()

    # create players
    print_decor(print)("Enter your name, please. ")
    human = Player(input('Name: '), 17)
    ai = Player("AI",17)

    print('Welcome, '+ human.name + '. Time to put some ships on the map!')
    time.sleep(2)
    print(human.name + ', your part of the game map is on the left. Let\'s choose, where to put the first ship')
   

    # print the game table
    #custom game table for each player - in case later on I would decide, that it would look different for each player
    human_table = Progress_table() 
    ai_table= Progress_table()
    Progress_table.print_game_progress(human_table.table, ai_table.table)

    place_ships(human)
    place_ships(ai)


    updated_human_table=human_table.table_to_print(human.ship_dictionary)
    
    Progress_table.print_game_progress(updated_human_table, ai_table.table)
 
    input("AI has made its ship selection. Random player will be selected to start. Are you ready?  [ANY input ot continue]")
    
    # create list of initial strike options
    human.strike_options = Ship_placement().options 
    ai.strike_options = Ship_placement().options  

    # create AI object  AI class contains all the decision making on follow up strikes
    AI_object = AI()

    if random.choice([1,2,3,4,5,6]) % 2 ==1:
        next_player = human
    else:
        next_player = ai
    while human.lives > 0 and ai.lives > 0:
        next_player = player_turn(next_player)
        updated_human_table=human_table.table_to_print(human.ship_dictionary,ai.strike_dictionary)
        updated_ai_table=ai_table.table_to_print(human.strike_dictionary)
        Progress_table.print_game_progress(updated_human_table, updated_ai_table)
        time.sleep(3)

    if human.lives == 0:
        print_decor(print_decor(print))("AI won the game... "+human.name + ", you\'ve got destroyed!")
    else:
        print_decor(print_decor(print))(human.name + ", you\'ve won the game!")
    
    while True: 
        try:
            
            decision = input("Rematch? [Y] - yes || [N] - no:")
            if decision.upper() not in ["Y","N"]:
                raise
            
            break
        except:
            print(decision +" is not a valid option. Try again: ")
            continue

    if decision.upper() == "Y":
        continue
    else:
        break

