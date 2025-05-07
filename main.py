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
 parser = argparse.ArgumentParser(description="Simple Expense Tracker-cli")
 parser.add_argument("add")
 parser.add_argument("--description" ,type=str,help="provide a description")
 parser.add_argument("--amount",type=int,help="provide the expense")
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
     
                
      
 required_files=  {"expenses.json":"{}","id_tracker":"0","total_expenses":"0","duplicate_checker":"{}"}
 load_dependencies(required_files)   # function responsible for creating required files
 action=  sys.argv[1]
 if action== "add":
     
  add_expense()
 elif action=="list":
     list_expense() 
 


       


main()