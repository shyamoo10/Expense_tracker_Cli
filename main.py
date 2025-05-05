import argparse
import json
import os
import datetime
import sys
date_time= str( datetime.datetime.now())
date=  date_time[:10]


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
 def add_expense():
    id=  id_tracker()
    old_data=  read_file("./expenses.json")
    
     
    data=  {"id":id,"description":args.description,"date":date,"expense":args.amount}
    old_data[id] =  data
    print(old_data)
    write_file("./expenses.json",old_data)
                
      
 required_files=  {"expenses.json":"{}","id_tracker":"id=0","total_expenses":"total=0"}
 load_dependencies(required_files)   # function responsible for creating required files
 action=  sys.argv[1]
 if action== "add":
     
  add_expense()
 


       


main()