import json
import random
import string
from pathlib import Path




class Bank:

    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exists")

    except Exception as err:
        print(f"An error occurred as {err}")


    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        nums = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + nums + spchar
        random.shuffle(id)
        return "".join(id)



    def CreateAccount(self):
        info = {
            "name": input("Enter your Name : "),
            "age": int(input("Enter your age : ")),
            "email": input("Enter your email : "),
            "pin": input("Enter 4 digit pin : "),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }

        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("Sorry you cannot create an account.")
        else:
            print("Account has been created successfully.")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please Note down your account number.")
                
            Bank.data.append(info)
            Bank.__update()

    def DepositMoney(self):
        acc_no = input("Please enter your account number : ").strip()
        pin = input("Please enter your pin : ").strip()
        
        userdata = [i for i in Bank.data if i['accountNo.'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Sorry No Data Found.")

        else:
            amount = int(input("How much do you want to deposit? --> "))
            
            if amount > 100000 or amount < 0:
                print("Sorry the amount is not specific. You can deposit below 100000 and above 0.")

            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("Amount Deposited Successfully.")


    def WithdrawMoney(self):
        acc_no = input("Please enter your account no : ").strip()
        pin = input("Please enter your pin : ")

        userdata = [i for i in Bank.data if i['accountNo.'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Sorry Data not Found")

        else:
            amount = int(input("Enter amount to withdraw : "))

            if amount > userdata[0]['balance']:
                print("Cannot withdraw this amount.")
                print(f"Your bank balance is {userdata[0]['balance']}")

            elif amount < 0:
                print("Invalid amount!")
            
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print(f"Sucessful Withdrawl of {amount}")
                print(f"Your remaining balance is {userdata[0]['balance']}")

    def ShowDetails(self):
        acc_no = input("Enter your account number : ")
        pin = input("Enter your pin : ")

        userdata = [i for i in Bank.data if i['accountNo.'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Sorry no data found")

        else:
            print("Your Information is : \n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")
                print("")

    def UpdateDetails(self):
        acc_no = input("Enter your account number : ")
        pin = input("Enter your pin : ")

        userdata = [i for i in Bank.data if i['accountNo.'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Sorry no data found")
        
        else:
            print("You cannot change your account number, age, balance")
            print("Fill the details to change or leave it empty if no change")

            newdata = {
                "name": input("Enter name to change or press enter to skip : "),
                "email": input("Enter your new email to change or press enter to skip : "),
                "pin": input("Enter new pin to change or press enetr to skip : ")
            }
            
            if newdata["name"] == "":
                newdata["name"] = userdata[0]["name"]
            if newdata["email"] == "":
                newdata["email"] = userdata[0]["email"]
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]["pin"]

            newdata['age'] = userdata[0]["age"]
            newdata['accountNo.'] = userdata[0]["accountNo."]
            newdata['balance'] = userdata[0]["balance"]

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("Details Updated Successfully.")
            print("Updated details are : \n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")
            

            
    def DeleteAccount(self):
        acc_no = input("Enter your account number : ")
        pin = input("Enter your pin : ")

        userdata = [i for i in Bank.data if i['accountNo.'] == acc_no and i['pin'] == pin]

        if not userdata:
            print("Sorry no such data found")
        
        else:
            check = input("Press y if you actually want to delete the account or press n : ")

            if check == "n" or check == "N":
                print("Passed.")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account Deleted Sucessfully.")
                Bank.__update()



user = Bank()


print("Press 1 to create an account.")
print("Press 2 to deposit money in your account.")
print("Press 3 to withrdaw money from your account.")
print("Press 4 for details.")
print("Press 5 to update your details.")
print("Press 6 to delete your account.")

check = int(input("Which operation would you like to perform? --> "))

if check == 1:
    user.CreateAccount()

if check == 2:
    user.DepositMoney()

if check == 3:
    user.WithdrawMoney()

if check == 4:
    user.ShowDetails()
    
if check == 5:
    user.UpdateDetails()

if check == 6:
    user.DeleteAccount()
