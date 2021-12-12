import sys
import os

# Dayeem Parkar GDC Software Engineering Fellowship programming task

# get arguments
arguments = sys.argv
argCount = len(arguments) - 1

# defining task and completed file paths
taskPath = os.path.join(sys.path[0], "task.txt")
completedPath = os.path.join(sys.path[0], "completed.txt")

# help function
def help():
    print('Usage :-')
    print('$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list')
    print('$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order')
    print('$ ./task del INDEX            # Delete the incomplete item with the given index')
    print('$ ./task done INDEX           # Mark the incomplete item with the given index as complete')
    print('$ ./task help                 # Show usage')
    print('$ ./task report               # Statistics')


# add task function
def add(priority, name):
    global taskPath
    
    insertData = ""
    toInsert = True
    
    # retrieve all tasks
    with open(taskPath, "a+") as taskf:
        # move to start of the file and go through lines
        taskf.seek(0)
        for line in taskf:
            line = line.strip()
            
            # insert our task at appropriate place based on priority
            firstSpace = line.find(' ')
            lp = int(line[:firstSpace])
            if toInsert and int(priority) < lp:
                line = priority + " " + name + "\n" + line
                toInsert = False
            insertData = insertData + line + "\n"
        
        if toInsert:
            insertData = insertData + priority + " " + name
        else:
            insertData = insertData[:len(insertData)-1]
        
        # truncate the file and insert modified data
        taskf.truncate(0)
        taskf.write(insertData)
        print('Added task: "' + name +  '" with priority ' + priority)
        
    taskf.close()


# display pending tasks
def pending():
    global taskPath
    index = 0
    
    # retrieve all tasks
    with open(taskPath, "a+") as taskf:
        # move to start of the file and go through lines
        taskf.seek(0)
        
        for line in taskf:
            index += 1
            line = line.strip()
            # seperate priority and name (including initial whitespace)
            firstSpace = line.find(' ')
            priority = line[:firstSpace]
            name = line[firstSpace:]
            print(str(index) + "." + name + " [" + priority + "]")
        if index == 0:
            print("There are no pending tasks!")
        
    taskf.close()


# complete task at given index
def complete(index):
    global taskPath, completedPath
    insertData = ""
    index -= 1
    toInsert = True
    
    # retrieve task at index from task.txt and insert it into completed.txt
    with open(taskPath, "a+") as taskf, open(completedPath, "a+") as compf:
        taskf.seek(0)
        
        for i, line in enumerate(taskf):
            line = line.strip()
            if i == index:
                firstSpace = line.find(' ')
                name = line[firstSpace+1:]
                if os.stat(completedPath).st_size==0:
                    compf.write(name)
                else:
                    compf.write("\n" + name)
                toInsert = False
                print("Marked item as done.")
            else:
                insertData = insertData + line + "\n"
        
        if toInsert:
            print("Error: no incomplete item with index #" + str(index + 1) + " exists.")
        
        taskf.truncate(0)
        taskf.write(insertData[:len(insertData)-1])
    
    taskf.close()
    compf.close()


# delete task at given index
def delete(index):
    global taskPath
    insertData = ""
    index -= 1
    toDelete = True
    
    # retrieve task at index from task.txt
    with open(taskPath, "a+") as taskf:
        taskf.seek(0)
        
        for i, line in enumerate(taskf):
            if i == index:
                toDelete = False
                print("Deleted task #" + str(i+1))
            else:
                insertData = insertData + line.strip() + "\n"
        
        if toDelete:
            print("Error: task with index #" + str(index + 1) + " does not exist. Nothing deleted.")
        
        taskf.truncate(0)
        taskf.write(insertData[:len(insertData)-1])
    
    taskf.close()


# retrieve all completed and pending tasks
def report():
    global taskPath, completedPath
    pCount = 0
    cCount = 0
    pTask = ""
    cTask = ""
    
    # retrieve pending from task.txt and completed from completed.txt
    with open(taskPath, "a+") as taskf, open(completedPath, "a+") as compf:
        taskf.seek(0)
        compf.seek(0)
        
        if os.stat(taskPath).st_size==0:
            print("Pending : 0")
        else:
            for line in taskf:
                pCount += 1
                line = line.strip()
                firstSpace = line.find(' ')
                priority = line[:firstSpace]
                name = line[firstSpace:]
                pTask = pTask + str(pCount) + "." + name + " [" + priority + "]\n"
            print("Pending :", pCount)
            print(pTask)
        
        if os.stat(completedPath).st_size==0:
            print("Completed : 0")
        else:
            for line in compf:
                cCount += 1
                line = line.strip()
                cTask = cTask + str(cCount) + ". " + line + "\n"
            print("Completed :", cCount)
            print(cTask[:len(cTask)-1])
    
    taskf.close()
    compf.close()


# go to different functions based on arguments
if argCount == 0:
    help()

elif argCount > 0:
    if arguments[1] == 'help':
        help()
    
    elif arguments[1] == 'ls':
        pending()
    
    elif arguments[1] == 'report':
        report()
    
    elif arguments[1] == 'add':
        if argCount == 3:
            add(arguments[2], arguments[3])
        else:
            print("Error: Missing tasks string. Nothing added!")
    
    elif arguments[1] == 'done':
        if argCount == 2:
            complete(int(arguments[2]))
        else:
            print("Error: Missing NUMBER for marking tasks as done.")
    
    elif arguments[1] == 'del':
        if argCount == 2:
            delete(int(arguments[2]))
        else:
            print("Error: Missing NUMBER for deleting tasks.")
