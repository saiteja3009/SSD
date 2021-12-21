import requests
import json
import random

from server import transaction
base = "http://localhost:8000/"
items = {}
order = {}
items_list = {}
total_amount = 0
isloggedin = False


def get_random():
    possible_discounts = [0, 10, 25, 50, -20]
    ''' 
    probabilties as mentioned in the requirements.
    '''
    probability = [20, 15, 10, 5, 50]
    return random.choices(possible_discounts, weights=(20, 15, 10, 5, 50))


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


'''These the functions which get or post from the server'''


def signup():
    username = input("Enter User Name")
    password = input("Enter Password")
    role = input("Role- Either chef/customer")
    request_app = {
        "username": username,
        "password": password,
        "role": role
    }
    res = requests.Session().post(
        'http://localhost:8000/signup', json=request_app).content
    print(res.decode('ascii'))
    return
    #res = requests.post('http://localhost:8000/create',json= {'id':id,'name':name,'stream':stream}).content


def login():
    global isloggedin
    username = input("Enter User Name")
    password = input("Enter Password")
    request_app = {
        "username": username,
        "password": password
    }
    res = requests.Session().post('http://localhost:8000/login', json=request_app).content
    if(res.decode('ascii') == "Logged in Succesful"):
        isloggedin = True
    print(res.decode('ascii'))
    return


def logout():
    res = requests.Session().get('http://localhost:8000/logout').content
    print(res.decode('ascii'))
    return


def get_menu():
    global items
    res = requests.Session().get('http://localhost:8000/getmenu').content
    if(res.decode('ascii') == "No Entries have been added yet"):
        print("No Entries have been added yet")
        return
    items = {}
    json_obj = json.loads(res)
    for i in json_obj:
        items[int(i)] = [json_obj[i]["half_plate_price"],
                         json_obj[i]["full_plate_price"]]
    # print(items)
    print("Item Id\tHalf_Price\tFull_Price")
    for i in items:
        print(i, items[i][0], items[i][1], sep="\t", end="\n")


def add_menu():
    item_id = int(input("Enter ID"))
    half_plate_price = int(input("Enter half_plate_price"))
    full_plate_price = int(input("Enter full_plate_price"))
    request_app = {
        'item_id': item_id,
        'half_plate_price': half_plate_price,
        'full_plate_price': full_plate_price
    }
    res = requests.Session().post(
        'http://localhost:8000/addmenu', json=request_app).content
    print(res.decode('ascii'))
    return


def order_item():
    global total_amount, items, items_list
    if items == {}:
        print("Check for new menu and order again")
    else:
        # print(items_list)
        total_amount = 0
        items_list = {}
        print("Enter the total number of different items to be ordered :")
        no_of_items = int(input())
        for i in range(no_of_items):
            print("Enter item id and 0 for half plate/ 1 for full plate")
            item_id = int(input())
            half_full_plate = int(input())
            print("Enter the quantity of above item")
            quantity = int(input())
            cost_per_single_quantity = float(items[item_id][half_full_plate])
            try:
                if half_full_plate == 0:
                    items_list[(item_id, "Half",
                                cost_per_single_quantity)] += quantity
                else:
                    items_list[(item_id, "Full",
                                cost_per_single_quantity)] += quantity
            except KeyError:
                if half_full_plate == 0:
                    items_list[(item_id, "Half",
                                cost_per_single_quantity)] = quantity
                else:
                    items_list[(item_id, "Full",
                                cost_per_single_quantity)] = quantity
            total_amount += cost_per_single_quantity*quantity


def get_bill():
    global items_list
    global total_amount
    print("Enter the tip percentage : 0/10/20")
    tip_percent = int(input())
    total_amount_after_tip = (total_amount)+(total_amount*tip_percent)/100
    print("Total amount is :", "%.2f" % total_amount_after_tip)
    print("Enter the total number of people")
    no_of_people = int(input())
    each_share = total_amount_after_tip/no_of_people
    print("Each share of a person is -", "%.2f" % each_share)

    '''
    Test your luck event
    '''

    discount_value = 0
    total_value = total_amount_after_tip
    print("Do you wish to participate in TEST YOUR LUCK EVENT, if yes enter 1, else 0")
    test_your_luck = int(input())
    if(test_your_luck == 1):
        get_random_discount = get_random()
        print()
        ''' 
        Printing the required pattern
        '''

        if(get_random_discount[0] > 0):
            print("Discount obtained is :", get_random_discount[0], end="%\n")
            print_discount_pattern()
            discount_value = -1*(total_amount_after_tip *
                                 get_random_discount[0])/100
            total_value = total_amount_after_tip+discount_value

        else:
            print("Better Luck Next time")
            print("Discount obtained is :", get_random_discount[0], end="%\n")
            print_no_dicount_pattern()
            discount_value = (total_amount_after_tip*-
                              get_random_discount[0])/100
            total_value = total_amount_after_tip+discount_value

    print("\n\tBILL\n")
    for i in items_list:
        print("Item", i[0], "[", i[1], "]", "[", items_list[i],
              "] :", "%.2f" % (i[2]*items_list[i]))
    print("Total:", "%.2f" % total_amount)
    tip_value = total_amount_after_tip-total_amount
    print("Tip Percentage:", tip_percent, "%")
    print("Discount/Increase:", "%.2f" % discount_value)
    print("Final Total:", "%.2f" % total_value)
    print()
    print("Each Person share of total value:", "%.2f" %
          (total_value/no_of_people))

    res = requests.post('http://localhost:8000/transaction', json={
        'total_amount': total_amount,
        'tip_percent': tip_percent,
        'discount_val': discount_value,
        'total_bill': total_value,
    }).content

    transaction_id = res.decode('ascii')
    orderSummary = []
    for i in items_list:
        if i[1] == "Half":
            orderSummary.append({
                                'item_id': i[0],
                                'type': 'Half',
                                'quantity': items_list[i]
                                })
        if i[1] == "Full":
            orderSummary.append({
                'item_id': i[0],
                'type': 'Full',
                'quantity': items_list[i]
            })

    requests.post('http://localhost:8000/itemlist', json={
        'transaction_id': transaction_id,
        'items_list': orderSummary
    })
    print("bill added to db successfully")
    items_list = {}
    total_amount = 0


def get_prev():
    res = requests.Session().get('http://localhost:8000/transac').content
    global items

    if items == {}:
        get_menu()
    obj = json.loads(res)
    if(len(obj) == 0):
        print("no transactions made yet")
        return
    else:
        print("Transaction id")
        for i in obj:
            print(obj[i]["transaction_id"], sep="\t\t", end="\n")
        choice = int(
            input("Enter the transaction id to view the bill and enter -1 to exit\n"))
        if choice == -1:
            return
        else:
            if 1 == 2:
                print("enter valid transaction id in the list")
            else:
                res = requests.Session().post('http://localhost:8000/transspe', json={
                    'transaction_id': choice,
                }).content
                json_obj = json.loads(res)
                order = json_obj['order']
                totalamount = json_obj['total_amount']
                discount_value = json_obj['discount_val']
                total_value = json_obj['total_bill']
                tip_percent = json_obj['tip_percent']
                # print(order)
                print("\n\tBILL\n")
                for i in order:
                    x = int(i)
                    # print(i,order[i][0],order[i][1])
                    if(order[i][0] == "Full"):
                        print("Item", i, "[", order[i][0], "]", "[", order[i][1], "] :", "%.2f" % (
                            int(order[i][1])*items[x][1]))
                    else:
                        print("Item", i, "[", order[i][0], "]", "[", order[i][1], "] :", "%.2f" % (
                            int(order[i][1])*items[x][0]))
                print("Total:", "%.2f" % totalamount)
                print("Tip Percentage:", tip_percent, "%")
                print("Discount/Increase:", "%.2f" % discount_value)
                print("Final Total:", "%.2f" % total_value)


'''Enter the choices accordingly'''

while(True):
    print("Select the choice:")
    print("1.SignUp")
    print("2.Login")
    print("3.Logout")
    print("4.Get Menu")
    print("5.Add to Menu")
    print("6.Order items")
    print("7.Get CurrentItems Bill")
    print("8.View Previous Bills")
    print("9.Exit")
    choice = int(input())
    if(choice == 1):
        signup()
    elif(choice == 2):
        login()
    elif(choice == 3 and isloggedin == True):
        logout()
        isloggedin = False
    elif(choice == 4 and isloggedin == True):
        get_menu()
    elif(choice == 5 and isloggedin == True):
        add_menu()
    elif(choice == 6 and isloggedin == True):
        order_item()
        print("Now enter 7 to get the bill")
    elif(choice == 7 and isloggedin == True):
        get_bill()
    elif(choice == 8 and isloggedin == True):
        get_prev()
    elif(choice == 9):
        break
    else:
        print("Enter correct choice and also make sure you are logged in")
