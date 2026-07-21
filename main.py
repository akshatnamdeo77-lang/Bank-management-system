from pathlib import  Path
import json
import random
import string

class bank:
    
    database="database.json"
    data=[]
    try:
        if Path(database).exists():
            with open(database,'r') as fs:
                data=json.loads(fs.read()) # yeh json string ko python list mein convert krti hai
    except Exception as err:
        print(f"An error occurred as {err} try again")
    @classmethod
    def __update(cls):
        with open (cls.database,'w') as fs:
            fs.write(json.dumps(cls.data,indent=4))  # naya data ,database mein chla gya 
    @staticmethod
    def __Generate_accountno():
            digits=random.choices(string.digits,k=12)    # charcaters generate krne ke liye eyhh use krna pdta hai char=random.choices(string.ascii_uppercase,k=4) 
            final="".join(digits)
            print(f"Your account number is {final}")
            return final 
                         #list ko string mein convert krna
            
    def create_account(self):
        info={
            "name":input("enter your name:- "),
            "age": int(input("enter your age:-")),
            "mail":input("enter your mail id:-"),
            "balance":0,
            "contact number":int(input("enter your contact number")),
            "pin":int(input("enter your 4 digit pin:-")),
            "account number":bank.__Generate_accountno()
        }
      
        try:
             while True:
                 if len(str(info["pin"]))!=4:
                    info["pin"]=int(input("you have entered wrong pin please try again"))
                 else :
                  break
                 
        except Exception as ValueError:
              print("you can only enter numbers!")

        try:
             while True:
         
               if len(str(info["contact number"]))!=10:
                  info["contact number"]=int(input("you have entered wrong number please try again : - "))
               else :
                   break
        except Exception as ValueError:
              print("you have entered wrong number please try again")
        
        if info["age"]<18:
            print("you are a minor")
            return
        else :
            bank.data.append(info)
            bank.__update()
            print("your account created sucessfully")
     
       
    def login(self):
                        accountno=input(("enter your account number:-"))
                        Pass=int(input("enter your pin:-"))
                        for i in self.data:
                            if  i["pin"]==Pass and i["account number"]==accountno:
                                print("login successful !!")
                                print(f"Welcome {i["name"]}!!")
                                return i
                             

                    
                        return None   

                     
    def deposit(self):
          user=self.login()
          if user is None:
               print("no such user exists!!")
               return
          else:
                amount=int(input("Enter the amount you want to deposit:-"))
                if amount>100000 or amount<=0:
                  print("you cannot deposit more than 100000 rs or less than zero rs!!")
                else:
                    user["balance"]+=amount
                    print(f"You have successfully deposite {amount}Rs!!")
                    bank.__update()
                    return

               
    def withdrawal(self):
         user=self.login()
         if user is None:
              print("no such user exists!!")
              return
         else:
              amount=int(input("Enter the amount you want to withdrawal(Rs):-"))
              if user["balance"]>amount:
                    user["balance"]-=amount
                    print(f"You have successfully withdrawn {amount}Rs !!")
                    print(f"Thank you for visiting {user["name"]}!!")
                    bank.__update()
                    return
              else:
                   print(f"insufficient balance!!")
                   return
    def checkdetails(self):
         user=self.login()
         if user  is None:
              print("no such user exists!!")
              return
         else:
              print(f" your details are:-")
              for i in user:
                   print(f"{i} :{user[i]}")
              bank.__update()
              return
            
    def update_details(self):
         user=self.login()
         if user is None:
              print("no such user exists!!")
              return
         else:
              print("enter what you want to update!! ")
              print("press 1 for updating name ")
              print("press 2 for updating mail ")
              print("press 3 for updating number ")
              print("press 4 for updating pin ")
              check=int(input("tell your response:-"))
              if check==1:
                   user["name"]=input("enter the name:-")
                   bank.__update()
                   print(f"name updated successfully!!{user["name"]}")
                   return
              if check==2:
                   user["mail"]=input("enter the mail:-")
                   bank.__update()
                   print(f"mail updated successfully!!{user["mail"]}")
                   return
              if check==3:
                         while True:
                              user["contact number"]=input("enter your number:-")
                              if len(str(user["contact number"]))!=10:
                                 user["contact number"]=input("contact number must contain exactly 10 digits! please try again : - ")
                              elif not user["contact number"].isdigit():
                                   print("Contact number should contain only Digits!!")
                              else:
                                   break
                         bank.__update()
                         print(f"phone number updated successfully!!{user["contact number"]}")
                         return
              if check==4:
                   while True:
                        user["pin"]=input("enter your pin:-")
                        if len(user["pin"])!=4:
                           user["pin"]=  input("pin must contain exactly 4 Digits !!pleasse try again:-")
                        elif not user["pin"].isdigit():
                             print("PIN must  contain only Digits!!")
                        else:
                             break
                   user["pin"]=int(user["pin"])
                   bank.__update()
                   print(f"pin updated successfully!!{user["pin"]}")
                   return
              else:
                   print("Invalid key entered!!")
                   return


    def delete(self):
         user=self.login()
         if user is None:
               print("no such user exists!!")
               return
         else:
               print("you only have three chances!!")
               accountno=input("enter your account number:-")
               count=0
               while(user["account number"]!=accountno):
                    if count>3:
                         print("you can only enter account number 3 times NO ACCOUNT DELETED!!!")
                         return
                    print("Account doesn't exists with this account number!!")
                    accountno=input("enter your account number:-")
                    count+=1
               self.data.remove(user)
               bank.__update()
               print("Account deleted successfully!!")
               return 
    def exit(self):
         print("Thank you for visiting!!")  
         return            
    



print("Press 1 for creating an account")
print("press 2 for depositing money")
print("press 3 for withdrawal")
print("press 4 for checking details")
print("press 5 for updating some details")
print("press 6 for deactivating your account")
print("press 0 for exit")

check=int(input("tell your response:-"))
obj=bank()
if check==1:
    obj.create_account()
elif check==2:
     obj.deposit()
elif check==3:
     obj.withdrawal()
elif check==4:
     obj.checkdetails()
elif check==5:
     obj.update_details()
elif check==6:
     obj.delete()
elif check==0:
    obj.exit()
else:
     print("You have entered invalid number!!")
     
     



