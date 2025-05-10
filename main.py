import argparse
import json
import os
import datetime
import sys

date_time= str( datetime.datetime.now())
date=  date_time[:10]
from prettytable import PrettyTable
table = PrettyTable()
 
def main(): 
 calender= {"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"}   
 def validate_month(value):
     ivalue =  int(value)
     if not ( ivalue >  0  and ivalue < 13):
         raise argparse.ArgumentTypeError("Please Provide a valid Month")
     return value
              
 def check_positve(value):
     ivalue=  int(value)
     if ivalue <=0 :
       raise argparse.ArgumentTypeError(f"Expense cant be a negative or zero")
     return  ivalue
 parser = argparse.ArgumentParser(description="Simple Expense Tracker-cli")
 
 subparsers = parser.add_subparsers(dest="command", help="Available commands")
 add_parser = subparsers.add_parser("add", help="Add an Expense")
 add_parser.add_argument("--description", type=str,help="Description for the Expense",required=True)
 add_parser.add_argument("--amount",type=check_positve, help="Expense",required=True)
 delete_parser=  subparsers.add_parser("delete",help="Delete an  Expense")
 delete_parser.add_argument("--id",type=str,help="Delete an Expense with the ID",required=True)
 summary_parser=  subparsers.add_parser("summary",help="To view the total expense")
 summary_parser.add_argument("--month",type=validate_month,help="To view the total expense for a particular month")
 subparsers.add_parser("list",help="To view the Information of Expenses in a tabular form")
     
 

 args=  parser.parse_args()
 ## reading data from a file 
 
 def read_file(path):
     try:
         with open(path,"r") as file:
            content=  file.read()
            deserialize_content=  json.loads(content)
            
            return deserialize_content
     except Exception as e :
         return e 
 def write_file(path,content):
     try:
         
      parsed_content=  json.dumps(content)
      with open(path,"w")  as file:
          file.write(parsed_content)
     except Exception as e :
         return  e     
     
 def id_tracker():
   id =  read_file("./id_tracker")
   int_id =  int(id)
   new_id=  int_id+1
   write_file("./id_tracker",new_id)
   return int_id
      
                
 #function for file creation
 def create_file(path,content):
   try:
          
    with open(path,"w")  as file:
        file.write(content)
   except Exception as e :
      return e
 def load_dependencies(files):
     for file  in  files:
         if   not  os.path.exists(file):
             create_file(file,files[file])
 def update_duplicates(data):
     duplicates=  read_file("./duplicate_checker")
     new_dupe=  {data["description"]:data["id"]}
     duplicates.update(new_dupe)
     write_file("./duplicate_checker",duplicates)           
 def add_expense():
    id=  id_tracker() 
        
    data=  {"id":id,"description":args.description,"date":date,"expense":args.amount}
    if duplicate_checker(data):
     return 
 
    
    old_data=  read_file("./expenses.json")
    
     
    
    old_data[id] =  data
    
    write_file("./expenses.json",old_data)
    update_duplicates(data)
    print(f" Expense added successfully (ID: {id})")
# function to handle duplicates 
 def duplicate_checker(expense):
      duplicates=  read_file("./duplicate_checker")
      if expense["description"] in duplicates :
          print(f"there exist a  copy of this with the id {duplicates[expense["description"]]}")
          return True
      return False
  
 def list_expense():
     table.field_names=  ["ID","Date","Description","Amount(INR)"]
     expenses=  read_file("./expenses.json")
     for expense_id in expenses:
         expense=  expenses[expense_id]
         
         table.add_row([expense["id"],expense["date"],expense["description"],expense["expense"]])
     print(table) 
     
 def total_expenses():
    expenses=  read_file("./expenses.json")
    
    total =0
    for key in expenses:
        
         value = expenses[key]
        
           
         total+= value["expense"]
    print(f"Total Expense : {total}")
 def format_month(month):
     if len(month)== 1:
         return f"0{month}"
     return month
           
 def total_expense_month(month):
     try:
           
           f_month=  format_month(month)
           month_words=  calender[f_month]
        #    print(f_month)
           expenses=  read_file("./expenses.json")
           
           sum=0
         
           for key in expenses:
             
             expense_month= expenses[key]["date"][5:7]  
             if expense_month== f_month:
                 sum+= expenses[key]["expense"]
           print(f"Total Expenses for {month_words}= {sum}")  
     except Exception as e :
         print(e)
                   
                 
                        
    
 def delete_expense(id):
     
    try:
            
      expenses=  read_file("./expenses.json")
      
      del_expense=  expenses[id]
      
      
      
      del(expenses[id])
      
      write_file("./expenses.json",expenses)
      # updating the duplicate checker
      duplicates=  read_file("./duplicate_checker")
      del(duplicates[del_expense["description"]])
      write_file("./duplicate_checker",duplicates)
      print(f"Expense deleted  successfully (ID: {id})")
     
        
    except :
             print(f"There is no data with the ID : {id}") 
     
                      
      
 required_files=  {"expenses.json":"{}","id_tracker":"1","duplicate_checker":"{}"}
 load_dependencies(required_files)   # function responsible for creating required files
 
 
 if args.command=="list":
     list_expense()
 elif args.command== "add":
        add_expense()
  
 
 elif args.command=="summary":
    
    if args.month:
             
      total_expense_month(args.month)
    else:
         total_expenses()      
 elif  args.command =="delete":
     
     delete_expense(args.id)
     
 elif args.command==None:
     print("Arguments cannot become empty!") 
     return
 else:
    print("command error , for the correct usage use help flag (--help or -h)")
    return 
 


       


main()