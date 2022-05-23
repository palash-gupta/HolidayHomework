from flask import Flask, render_template, redirect, render_template_string, request
import pickle

app = Flask(__name__)

fields = ["name", "rollNo", "marks"]
fieldsSentenceCase = ["Name", "Roll No.", "Marks"]

fileOpened = False
file = None
options = ["initialise", "insert", "update", "search", "delete", "close"]


@app.route("/")
def index():
    return render_template("index.html", options=options, fileOpened=fileOpened)


@app.route("/initialise/")
def initialise():
    if not fileOpened:
        return render_template("initialise.html", options=options, fileOpened=fileOpened)
    return redirect('/')


@app.route("/initialise/submit/", methods=["POST"])
def initialiseSubmit():
    global file
    file = open(request.form["filename"], "ab+")
    global fileOpened
    fileOpened = True

    return redirect("/")

@app.route('/insert/')
def insert():
    if fileOpened:
        return render_template("insert.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase)
    return redirect('/')
    
@app.route('/insert/submit/', methods=["POST"])
def insertSubmit():
    global file
    
    record = request.form.to_dict()

    file.seek(0)

    if len(file.read()) == 0:
        pickle.dump(record, file)
        return render_template("insert.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase)

    try:
        file.seek(0)
        tmp = []
        doneOnce = False

        while True:
            rec = pickle.load(file)
            if rec["name"] > record["name"] and not doneOnce:
                tmp.append(record)
                doneOnce = True

            tmp.append(rec)

    except EOFError:
        if not doneOnce:
            tmp.append(record)

        file.truncate(0)

        for i in tmp:
            pickle.dump(i, file)

        return redirect('/insert/')


@app.route('/update/')
def update():
    if fileOpened:
        return render_template("update.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase)
    return redirect('/')

@app.route('/update/submit/', methods=["POST"])
def updateSubmit():
    global file

    requestForm = request.form.to_dict()
    searchKey, newValues = {}, {}

    for i in range(len(fields)):
        searchKey[fields[i]] = requestForm[fields[i]]
        newValues[fields[i]] = requestForm[f"new{fields[i]}"]

    file.seek(0)

    try:
        tmp = []

        while True:
            rec = pickle.load(file)
            newRec = rec.copy()
            allCorrect = True
            for field in searchKey.keys():
                newRec[field] = (
                    newValues[field] if newValues[field] != "" else rec[field]
                )
                if searchKey[field] == "":
                    continue

                if rec[field] != searchKey[field]:
                    allCorrect = False
                    break

            tmp.append(newRec if allCorrect else rec)

    except EOFError:
        file.truncate(0)

        for i in tmp:
            pickle.dump(i, file)

        return redirect('/update/')

@app.route('/search/')
def search():
    if fileOpened:
        return render_template("search.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase)
    return redirect('/')

@app.route('/search/submit/', methods=["POST"])
def searchSubmit():
    global file
    searchKey = request.form.to_dict()

    file.seek(0)
    records = []

    try:
        while True:
            rec = pickle.load(file)
            allCorrect = True
            for field in searchKey.keys():
                if searchKey[field] == "":
                    continue

                if rec[field] != searchKey[field]:
                    allCorrect = False
                    break

            if allCorrect:
                records.append(rec)
    except EOFError:
        return render_template("search_results.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase, records=records)



@app.route('/delete/')
def delete():
    if fileOpened:
        return render_template("delete.html", options=options, fileOpened=fileOpened, fields=fields, fieldsSentenceCase=fieldsSentenceCase)
    return redirect('/')

@app.route('/delete/submit/', methods=["POST"])
def deleteSubmit():
    global file
    searchKey = request.form.to_dict()

    file.seek(0)

    try:
        tmp = []
        while True:
            rec = pickle.load(file)
            allCorrect = True
            for field in searchKey.keys():
                if searchKey[field] == "":
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

    return redirect('/delete/')

    
@app.route("/close/")
def close():
    global fileOpened
    if fileOpened:
        global file
        file.close()
        fileOpened = False
        return redirect("/")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
