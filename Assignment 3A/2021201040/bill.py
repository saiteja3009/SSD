import csv
import random

''' 
Function definations which are used in the program like printing patterns etc
'''

def get_random():
    possible_discounts = [0,10,25,50,-20]
    ''' 
    probabilties as mentioned in the requirements.
    '''
    probability = [20,15,10,5,50]
    return random.choices(possible_discounts,weights = (20,15,10,5,50))

def print_discount_pattern():
    print(" ****            **** ")
    print("|    |          |    |")
    print("|    |          |    |")
    print("|    |          |    |")
    print(" ****            **** \n")
    print("          {}")
    print("    ______________")

def print_no_dicount_pattern():
    print(" ****")
    print("*    *")
    print("*    *")
    print("*    *")
    print("*    *")
    print(" ****")


file_name = "Menu.csv"
fields = []
rows = []

''' 
Reading the Menu using csv filereader
'''

with open(file_name,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

''' 
Printing the Menu 
'''

for i in range(len(fields)):
    print(fields[i],end = " ")
print()
for i in range(len(rows)):
    for j in range(3):
        print(rows[i][j],end=" \t")
    print()

''' 
Taking the order from the user
and required details about the order
'''


'''
item_lists stores the item along with the quantity of
that particular item and total_amount stores the total
'''

total_amount = 0
items_list = {}
print("Enter the total number of different items to be ordered :")
no_of_items = int(input())
for i in range(no_of_items):
    print("Enter item id and 1 for half plate/ 2 for full plate")
    item_id = int(input())
    half_full_plate = int(input())
    print("Enter the quantity of above item")
    quantity = int(input())
    cost_per_single_quantity = float(rows[item_id-1][half_full_plate])
    try:
        if half_full_plate == 1:
            items_list[(item_id,"Half",cost_per_single_quantity)] += quantity
        else:
            items_list[(item_id,"Full",cost_per_single_quantity)] += quantity
    except KeyError:
        if half_full_plate==1:
            items_list[(item_id,"Half",cost_per_single_quantity)] = quantity
        else:
            items_list[(item_id,"Full",cost_per_single_quantity)] = quantity
    total_amount += cost_per_single_quantity*quantity

'''
Calculating the total amount of bill including tip
and the share of each person
'''

print("Enter the tip percentage : 0/10/20")
tip_percent = int(input())
total_amount_after_tip = (total_amount)+(total_amount*tip_percent)/100
print("Total amount is :","%.2f" % total_amount_after_tip)
print("Enter the total number of people")
no_of_people = int(input())
each_share = total_amount_after_tip/no_of_people
print("Each share of a person is -","%.2f" % each_share)

'''
Test your luck event
'''

discount_value = 0
total_value = total_amount_after_tip
print("Do you wish to participate in TEST YOUR LUCK EVENT, if yes enter 1, else 0")
test_your_luck = int(input())
if(test_your_luck == 1):
    ''' 
    Getting random discount using random
     function generator
    '''
    get_random_discount = get_random()
    print()
    ''' 
    Printing the required pattern
    '''

    if(get_random_discount[0]>0):
        print("Discount obtained is :",get_random_discount[0],end="%\n")
        print_discount_pattern()
        discount_value = -1*(total_amount_after_tip*get_random_discount[0])/100
        total_value = total_amount_after_tip+discount_value
        
    else:
        print("Better Luck Next time")
        print("Discount obtained is :",get_random_discount[0],end="%\n")
        print_no_dicount_pattern()
        discount_value = (total_amount_after_tip*-get_random_discount[0])/100
        total_value = total_amount_after_tip+discount_value
        

'''
Printing the bill
'''

print("\n\tBILL\n")
for i in items_list:
    #print(i)
    print("Item",i[0],"[",i[1],"]","[",items_list[i],"] :","%.2f"%(i[2]*items_list[i]))
print("Total:","%.2f" % total_amount)
tip_value = total_amount_after_tip-total_amount
print("Tip Percentage:",tip_percent,"%")
print("Discount/Increase:","%.2f" % discount_value)
print("Final Total:","%.2f" % total_value)
print()
print("Each Person share of total value:","%.2f" % (total_value/no_of_people))






