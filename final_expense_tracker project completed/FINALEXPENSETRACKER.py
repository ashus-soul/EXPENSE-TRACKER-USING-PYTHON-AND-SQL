#db connection to python
import sqlite3
conn=sqlite3.connect("expenserecord.db")
cur=conn.cursor() #cursor to interact with db
cur.execute('''CREATE TABLE IF NOT EXISTS records(category TEXT,ItemName TEXT ,Amount INTEGER, WalletBalance INTEGER)''')
user_response=input("DO YOU WANT TO RUN EXPENSE TRACKER😎🎯🎯 , ENTER Y for YES : ")

#check if user want to use app
while user_response=="Y" or user_response=="y":
    print("***🎯🎯😎 EXPENSE TRACKER IS RUNNING 😎  🎯🎯***")
    
    print("ENTER 1 : ADD  AMOUNT IN WALLET\n")
    print("ENTER 2 : ADD SPENDINGS\n")
    print("ENTER 3 : RECORDS \n")
    print("ENTER 4 : EXIT THE PROGRAM 😒 \n ")
    op=int(input("ENTER YOUR DESIRED OPERATION : "))

    # 1. Grab the wallet balance from the database FIRST so all operations have the latest amount
    cur.execute("SELECT WalletBalance FROM records ORDER BY ROWID DESC LIMIT 1")
    last_record = cur.fetchone()

    # Set to 0 if it's the very first time
    current_balance = last_record[0] if last_record and last_record[0] is not None else 0

    # ==========================================
    # OPERATION 1: WALLET TOP-UP
    # ==========================================
    if op==1:
        # 2. Ask user if they want to override the database balance
        wb = input("DO YOU WANT TO MODIFY YOUR CURRENT BALANCE? (Y/N): ")
        if wb.lower() == 'y':
            current_balance = int(input("ENTER YOUR NEW WALLET AMOUNT : "))
            # Adding a quick insert here so your new balance actually saves to the DB!
            cur.execute("INSERT INTO records (category, ItemName, Amount, WalletBalance) VALUES (?, ?, ?, ?)", ("BALANCE UPDATE", "Wallet", 0, current_balance))
            conn.commit()
        else:
            print("NO MODIFICATION HAS BEEN MADE \n")

    # ==========================================
    # OPERATION 2: ADD EXPENSES
    # ==========================================
    elif op==2:
        #this block for category
        print("TELL US ABOUT YOUR SPENDING 🤑🤑")
        x=int(input("ENTER 1 FOR SHOPPING🛒 , ENTER 2 FOR FOOD🍉🍎 , ENTER 3 FOR ENTERTAINMENT🎮 , ENTER 4 FOR SOCIAL❤️ : "))
        cg=""
        if x==1:
            cg="SHOPPING"
        elif x==2:
            cg="FOOD"
        elif x==3:
            cg="ENTERTAINMENT"
        elif x==4:
            cg="SOCIAL"
        else:
            print("INVALID OPTION!!!🔒")
        #category block eneded

        #ITEM DETAILS
        item_name=input("ENTER NAME OF ITEM : " )
        item_price=int(input("ENTER AMOUNT OF ITEM : "))
        
        # 3. Do the math to decrease the balance
        new_balance = current_balance - item_price
        if new_balance<=0:
            print("insufficient balance , payment failed \n")
        else:
            #inserting data into table (database)
            #cur.execute("INSERT INTO records (category,ItemName,Amount) VALUES (cg,item_name,item_price)")
            #cur.execute("SELECT * FROM records")

            cur.execute("INSERT INTO records (category, ItemName, Amount,WalletBalance ) VALUES (?, ?, ?,?)", (cg, item_name, item_price,new_balance))
            conn.commit()

    # ==========================================
    # OPERATION 3: VIEW DB RECORDS
    # ==========================================
    elif op==3:
        #fetchall() is a method used on a database cursor object to retrieve all remaining rows of a query result set
        cur.execute("SELECT * FROM records")

        # 1. Grab all the data the database just found
        my_table_data = cur.fetchall()
        #print (my_table_data) -> very messy output so we use for loop for clean output

        # 2. Print it out line by line so you can actually see it
        print("--- YOUR EXPENSE RECORDS ---")

        #structure
        print("category ,ItemName  ,Amount, WalletBalance ")

        for row in my_table_data:
            print(row)

        print("\n")

    # ==========================================
    # OPERATION 4: EXIT
    # ==========================================
    elif op==4:
        # Breaks the while loop so you can escape
        user_response = "N"

    # ==========================================
    # CATCH-ALL FOR DUMB INPUTS
    # ==========================================
    else:
        print("INVALID OPERATION CHOSEN! TRY AGAIN. 😡\n")

else:
    print("MONEY TRACKER STOPED WORKING , YOUR DATA IS SECURED ")

#cur.execute("DELETE FROM records") #-> this line to delete db
#conn.commit()

conn.close()
#work COMPLETED !!!!!!!!!!!!!!!!!!!!