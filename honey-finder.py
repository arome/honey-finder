import os, datetime, timeit, shutil, time, sys
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
        print("Scanned " + str(numFiles) + (" entries" if numFiles > 1 else " entry")+" in " + "{:10.2f}".format(time) + " second" + ("s." if time > 1 else "."))
    else:
        print("Scanning " + str(numFiles) + (" entries" if numFiles > 1 else " entry")+" in the directory " + dirpath + ")"
    print(statusBar(currentPosition, 0 if time else 1))
    if not errorsFound:
        print("No entry found for " + name + (" between " + sdate + " and " + edate if sdate is not None else ""))  
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
    is_accessible = os.access(dirpath + filename,os.F_OK) #Check if you have access, this should be a path
    if is_accessible == True: #If you don't, create the path
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
        if dirpath[-1] != "\\":
            dirpath += "\\"
        limitToXML = 1 if input("Only search XML files? (y/n) : ").lower() == "y" else 0
        question = "Text you're searching for? : "
    sbyDate = 1 if input("Search by date? (y/n) : ").lower() == "y" else 0
    sdate, edate = None, None
    if sbyDate:
        sdate = datetime.datetime.strptime(input("Enter Date in (yyyy-mm-dd) format: "), "%Y-%m-%d")
        edate = sdate + datetime.timedelta(days=1) 
        after_date = time.mktime(sdate.timetuple())
        before_date = time.mktime(edate.timetuple())
    name = input(question)

    start_time = timeit.default_timer()

    currentPercentage, count = 0, 0
    errorsFound = []
    try:
        numFiles = len(os.listdir(dirpath))
        fileFound = []
        for filename in os.listdir(dirpath):
            if "." in filename and (not limitToXML or filename.endswith("xml")):
                if sbyDate:
                    if os.path.getmtime(dirpath+filename) > after_date and os.path.getmtime(dirpath+filename) < before_date:
                        filename = searchFileContent(dirpath, filename, name)
                else:
                    filename = searchFileContent(dirpath, filename, name)
                if filename is not None:
                    errorsFound.append(filename)
            if currentPercentage < int(count*100/numFiles):
                printCurrentState(dirpath, name, sdate, edate, numFiles, int(count*100/numFiles), errorsFound, 0)
                currentPercentage = count*100/numFiles
            count+=1

        end_time = timeit.default_timer()
        runTime = end_time - start_time
        printCurrentState(dirpath, name, sdate, edate, numFiles, int(count*100/numFiles)+4, errorsFound, runTime)
    except FileNotFoundError as err:
        if "network" in str(err):
            print("Make sure you are connected to the company's VPN.")
        else:
            print("This directory is not found")
    except PermissionError as perm:
        print("Missing permission to access:", perm)
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        print("The execution will now be terminated")

if __name__ == "__main__":
    main()