import pickle


fields = ["name", "rollNo", "marks"]
fieldsSentenceCase = ["Name", "Roll No.", "Marks"]

def main():
    help()
    fileOpened = False
    while True:
        choice = input("Enter Choice: ")

        if fileOpened:
            if choice == "0":
                print("File already opened! Close to open new file (5)")
            elif choice == "1":
                record = getRecord()
                insert(file, record)
            elif choice == "2":
                print("Update Values with which keys and values? (Press enter to skip a field)")
                searchKey, newValues = getSearchKeysAndValues()
                update(file,searchKey, newValues)
            elif choice == "3":
                search(file, getSearchKeys())
            elif choice == "4":
                delete(file, getSearchKeys())
            elif choice == "5":
                file.close()
                fileOpened = False                    
            elif choice == "h":
                help()
            elif choice == "s":
                file.seek(0)
                try:
                    while True:
                        print(pickle.load(file))
                except EOFError:
                    continue
            else:
                print("Invalid")
                continue

        else:
            if choice == "0":
                fName = input("Enter name of file (will be created if it doesn't exist) : ")
                file = open(fName, 'ab+')
                fileOpened = True
            elif choice == "5":
                print("No file open!")
            elif choice in list(map(str, list(range(1, 5)))):
                print("No file initialised! Initialise File (0)")
            else:
                print("Invalid")
                continue
        
def help():
    print("0: Initialise File\n1: Insert Entry\n2: Update Entry\n3: Search Entry\n4: Delete Entry\n5: Close File\nh: Help")

def getRecord():
    ret = {}
    for i in range(len(fields)):
        ret[fields[i]] = input(f"Enter {fieldsSentenceCase[i]}: ")

    return ret

def getSearchKeysAndValues():
    searchKeys = {}
    values = {}
    for i in range(len(fields)):
        searchKeys[fields[i]] = input(f"Look for {fieldsSentenceCase[i]}: ")
        values[fields[i]] = input(f"New Value for {fieldsSentenceCase[i]}: ")

    return searchKeys, values

def getSearchKeys():
    searchKeys = {}
    for i in range(len(fields)):
        searchKeys[fields[i]] = input(f"Look for {fieldsSentenceCase[i]}: ")

    return searchKeys

def insert(file, record):
    file.seek(0)

    if len(file.read()) == 0:
        pickle.dump(record, file)
        return 0

    try:
        file.seek(0)
        tmp = []
        doneOnce = False

        while True:
            rec = pickle.load(file)
            if rec['name'] > record['name'] and not doneOnce:
                tmp.append(record)
                doneOnce = True

            tmp.append(rec)

    except EOFError:
        if not doneOnce:
            tmp.append(record)
        
        file.truncate(0)

        for i in tmp:
            pickle.dump(i, file)


def update(file, searchKey, newValues):
    file.seek(0)

    try:
        tmp = []

        while True:
            rec = pickle.load(file)
            newRec = rec.copy()
            allCorrect = True
            for field in searchKey.keys():
                newRec[field] = newValues[field] if newValues[field] != '' else rec[field]
                if searchKey[field] == '':
                    continue

                if rec[field] != searchKey[field]:
                    allCorrect = False
                    break

            tmp.append(newRec if allCorrect else rec)

    except EOFError:
        file.truncate(0)

        for i in tmp:
            pickle.dump(i, file)

def search(file, searchKey):
    file.seek(0)

    try:
        found = False
        while True:
            rec = pickle.load(file)
            allCorrect = True
            for field in searchKey.keys():
                if searchKey[field] == '':
                    continue

                if rec[field] != searchKey[field]:
                    allCorrect = False
                    break

            if allCorrect:
                print(rec)
                found = True
    except EOFError:
        if not found:
            print("No records found")


def delete(file, searchKey):
    file.seek(0)

    try:
        tmp = []
        while True:
            rec = pickle.load(file)
            allCorrect = True
            for field in searchKey.keys():
                if searchKey[field] == '':
                    continue

                if rec[field] != searchKey[field]:
                    allCorrect = False
                    break

            if not allCorrect:
                tmp.append(rec)
    except EOFError:
        file.truncate(0)

        for i in tmp:
            pickle.dump(i, file)

if __name__ == '__main__':
    main()
