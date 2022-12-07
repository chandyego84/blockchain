from flask import Flask, render_template, redirect, url_for, request
from blockchain import Block, Blockchain

app = Flask(__name__)
appChain = Blockchain()

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def ActionResult():
    if request.method == 'POST':
        requestAction = request.form

        if 'New Transaction' in requestAction:
            return redirect(url_for('NewTransaction'))
        
        elif 'Mine' in requestAction:
            return redirect(url_for('Mine'))

        return render_template("home.html")

@app.route('/transactions/new')
def NewTransaction():
    print("We are making a transaction")

    return render_template('newTransaction.html')

@app.route('/mine')
def Mine():
    print("We are mining.")


    return render_template('mining.html')

    


        
if __name__ == '__main__':
    app.run(debug=True)