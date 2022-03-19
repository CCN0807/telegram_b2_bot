def card_value(c):
    x = ''
    if(c[1] == 0):
        x = '♦️'    
    elif(c[1] == 1):
        x = '♣️'
    elif(c[1] ==2):
        x = '♥️'
    else:
        x = '♠️'
    return f'{c[0]}{x}'

def card_list_value(list):
    val_list = []
    for c in list:
        val_list.append(card_value(c))
    return val_list

def display_value(list):
    val_list = []
    for c in list:
        x = ''
        if(c[1] == 0):
            x = '♦️'    
        elif(c[1] == 1):
            x = '♣️'
        elif(c[1] ==2):
            x = '♥️'
        else:
            x = '♠️'

        if(c[0] == 0):
            k= 'A'
            val_list.append(f'{k}{x}')
        elif(c[0] == 1):
            k= "dee"
            val_list.append(f'{k}{x}')
        elif(c[0] == 10):
            k = "Jack"
            val_list.append(f'{k}{x}')

        elif(c[0] == 11):
            k == "Queen"
            val_list.append(f'{k}{x}')

        elif(c[0] == 12):
            k = "King"
            val_list.append(f'{k}{x}')
        else:
            val_list.append(f'{c[0]}{x}')
    return val_list

def checkConsecutive(l):
    tmp = []
    for L in l:
        tmp.append(L[0])
    return sorted(tmp) == list(range(min(tmp), max(tmp)+1))

def check_flower(l):
    f = l[0][1]
    for i in l:
        if(i[1] != f):
            return False
    return True
def check_three_two(list):
    unique_list = []
    number_list = []
    for c in list:
        if c[0] not in unique_list:
            unique_list.append(c[0])
            number_list.append(1)
        else:
            number_list[unique_list.index(c[0])] += 1

    if(len(unique_list) == 2):
        appear_max_number = max(number_list)
        if(appear_max_number == 3):
            return 1200 + unique_list[number_list.index(appear_max_number)]*10
        elif(appear_max_number == 4):
            return 1600 + unique_list[number_list.index(appear_max_number)]*10
    else:
        return 0
def five_cards_checker(list):
    consective = checkConsecutive(list)
    if(not consective):
        for c in list:
            if(c[0] == 0):
                c[0] = 13
            if(c[0] == 1):
                c[0] = 14
        consective = checkConsecutive(list)
    
    same_flower = check_flower(list)
    number_max = 0
    flower_max = 0
    for c in list:
        if(c[0] == 0):
            c[0] = 13
        if(c[0] == 1):
            c[0] = 14
        if(c[0] > number_max):
            number_max = c[0]
            flower_max = c[1]
        
    if(consective and same_flower):
        return 10000 + number_max*10 + flower_max
    if(consective):
        return 400 + number_max*10 + flower_max
    if(same_flower):
        return 800 + number_max*10 + flower_max

    return check_three_two

def check_valid(list, previous = []):
    if(len(list) == 5):
        lis_value = five_cards_checker(list)
        if(five_cards_checker(list) == 0):
            return [False, "Invalid card combanition"]
        if(previous):
            previous_value = five_cards_checker(previous)
            lis_value = five_cards_checker(list)
            if(lis_value > previous_value):
                return [True, f"Valid input current: {lis_value} previous: {previous_value}"]
            else:
                return [False, f"input smaller than previous input current: {lis_value} previous: {previous_value}"]
        else:
            return [True, f"Valid input and no previous {lis_value}"]
    current_max = 0
    previous_max = 0
    for c in list:
        if(c[1] >= current_max):
            current_max = c[1]
        if(c[0] == 0):
            c[0] = 13
        if(c[0] == 1):
            c[0] = 14
    if(previous):
        for p in previous:
            if(p[0] == 0):
                p[0] = 13
            if(p[0] == 1):
                p[0] = 14
            if(p[1] >= previous_max):
                previous_max = p[1]
    if(len(list) == 1):
        if(previous):
            lis_value = list[0][0]*10 + list[0][1]
            previous_value = previous[0][0]*10 + previous[0][1]
            if(lis_value > previous_value): 
                return [True, f"Is valid, current: {lis_value} previous: {previous_value}"]
            else: 
                return [False, "This card is smaller than the previous card"]
        else:
            return [True, "No previous and valid"]
    elif(len(list) == 2):
        if(list[0][0] != list[1][0]):
            return [False, "number value of two cards are differnent"]
        if(previous):
            lis_value = list[0][0]*10 + current_max
            previous_value = previous[0][0]*10 + previous_max
            if(lis_value > previous_value): 
                return [True, "Is valid"]
            else: 
                return [False, "This card is smaller than the previous card"]
        else:
            return [True, "No previous and valid"]
    elif(len(list) == 3):
        if(list[0][0]!=list[1][0] or list[1][0] != list[2][0]):
            return [False, "The number value is different"]
        if(previous):
            lis_value = list[0][0]*10 + current_max
            previous_value = previous[0][0]*10 + previous_max
            if(lis_value > previous_value): 
                return [True, "Is valid"]
            else: 
                return [False, "This card is smaller than the previous card"]
        else:
            return [True, "No previous and valid"]
    elif(len(list) == 4):
        if(list[0][0]!=list[1][0] or list[1][0] != list[2][0] or list[2][0] != list[3][0]):
            return [False, "The number value is different"]
        if(previous):
            lis_value = list[0][0]*10 + current_max
            previous_value = previous[0][0]*10 + previous_max
            if(lis_value > previous_value): 
                return [True, "Is valid"]
            else: 
                return [False, "This card is smaller than the previous card"]
        else:
            return [True, "No previous and valid"]
