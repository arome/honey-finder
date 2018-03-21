import os, datetime, timeit, shutil, time 
clear = lambda: os.system('cls')

#times = '8:50'
#before_time = time.mktime(datetime.datetime.strptime(date+'/'+times, "%d/%m/%Y/%H:%M").timetuple())

def printWelcome():
    welcomeMessage = '''
    /$$   /$$                                               /$$$$$$$$ /$$                 /$$                    
    | $$  | $$                                              | $$_____/|__/                | $$                    
    | $$  | $$  /$$$$$$  /$$$$$$$   /$$$$$$  /$$   /$$      | $$       /$$ /$$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$ 
    | $$$$$$$$ /$$__  $$| $$__  $$ /$$__  $$| $$  | $$      | $$$$$   | $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
    | $$__  $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  | $$      | $$__/   | $$| $$  \ $$| $$  | $$| $$$$$$$$| $$  \__/
    | $$  | $$| $$  | $$| $$  | $$| $$_____/| $$  | $$      | $$      | $$| $$  | $$| $$  | $$| $$_____/| $$      
    | $$  | $$|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$      | $$      | $$| $$  | $$|  $$$$$$$|  $$$$$$$| $$      
    |__/  |__/ \______/ |__/  |__/ \_______/ \____  $$      |__/      |__/|__/  |__/ \_______/ \_______/|__/      
                                            /$$  | $$                                                            
                                            |  $$$$$$/                                                            
                                            \______/                                                              
    '''
    print(welcomeMessage)

def printCurrentState(name, sdate, edate, numFiles, currentPosition, errorsFound, time):
    clear()
    if time:
        print("Scanned " + str(numFiles) + " entries in " + "{:10.2f}".format(time) + " second" + ("s." if time > 1 else "."))
    else:
        print("Scanning " + str(numFiles) + " entries in the errors log...")
    print(statusBar(currentPosition, 0 if time else 1))
    if not errorsFound:
        print("No entries found for " + name + (" between " + sdate + " and " + edate if sdate is not None else ""))  
    else:
        print(str(len(errorsFound)) + " error" + ("s" if len(errorsFound) > 1 else "") + " found for " + name + (" between " + sdate + " and " + edate if sdate is not None else "")) 
        print(errorsFound)

def statusBar(num, showPercentage):
    bar = '['
    for x in range(num):
        bar +='#'
    restOfBar = 104-num
    if showPercentage:
        percentage = str(num) +'% '
        bar += ' '+ percentage
        restOfBar -= (len(percentage)+1)
    for x in range(restOfBar):
        bar += ' '
    bar += ']'
    return bar

def searchFileContent(dirpath, filename, name):
    with open(dirpath + filename,'r') as f:
        if name in f.readline():
            return filename

def main():
    printWelcome()
    dirpath = "\\\\10.104.5.45\\Elmah.Errors\\"
    customDir = 1 if input("Do you want to use a custom directory? (y/n) : ").lower() == "y" else 0
    question = "Which user are you looking for? : " 
    limitToXML = 0
    if customDir:
        dirpath = input("Please enter the path to your directory : ")
        limitToXML = 1 if input("Only search XML files? (y/n) : ").lower() == "y" else 0
        question = "Text you're searching for? : "
    sbyDate = 1 if input("Search by date? (y/n) : ").lower() == "y" else 0
    sdate, edate = None, None
    if sbyDate:
        sdate = datetime.datetime.strptime(input("Enter Date in (yyyy-mm-dd) format: "), "%Y-%m-%d")
        edate = sdate + datetime.timedelta(days=1) 
        print(sdate.timetuple())
        after_date = time.mktime(sdate.timetuple())
        before_date = time.mktime(edate.timetuple())
    name = input(question)

    start_time = timeit.default_timer()

    currentPercentage, count = 0, 0
    errorsFound = []
    numFiles = len(os.listdir(dirpath))
    for filename in os.listdir(dirpath):
        if not limitToXML or filename.endswith("xml"):
            if sbyDate:
                if os.path.getmtime(dirpath+filename) > after_date and os.path.getmtime(dirpath+filename) < before_date:
                    copyfile(dirpath+filename, "./temp/"+filename)
                    # filename = searchFileContent(dirpath, filename, name)
            else:
                filename = searchFileContent(dirpath, filename, name)
            if filename is not None:
                errorsFound.append(filename)
        if currentPercentage < int(count*100/numFiles):
            printCurrentState(name, sdate, edate, numFiles, int(count*100/numFiles), errorsFound, 0)
            currentPercentage = count*100/numFiles
        count+=1

    end_time = timeit.default_timer()
    time = end_time - start_time
    printCurrentState(name, sdate, edate, numFiles, int(count*100/numFiles)+4, errorsFound, time)

if __name__ == "__main__":
    main()