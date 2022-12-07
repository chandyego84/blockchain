from flask import Flask, render_template, redirect, url_for, request
from blockchain import Block, Blockchain

app = Flask(__name__)
appChain = Blockchain()

@app.route('/')
def HomePage():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def HomeActionResult():
    if request.method == 'POST':
        requestAction = request.form

        if 'New Transaction' in requestAction:
            return redirect(url_for('NewTransactionPage'))
        
        elif 'Mine' in requestAction:
            return redirect(url_for('MinePage'))

        return render_template("home.html")

@app.route('/transactions/new')
def NewTransactionPage():
    print("A new transaction is being made")

    return render_template('newTransaction.html')

@app.route('/transactions', methods=['POST', 'GET'])
def NewTransaction():
    if request.method == 'POST':
        requestAction = request.form

        # get transaction info from the request
        sender = requestAction['Sender']
        recipient = requestAction['Recipient']
        amount = requestAction['Amount']

        appChain.NewTransaction(sender, recipient, amount)
        transactions = appChain.currentTransactions

        return render_template('transactions.html', requestAction=requestAction, transactions=transactions)


@app.route('/mine')
def MinePage():
    print("We are mining.")
    
    return render_template('mining.html')

    
if __name__ == '__main__':
    app.run(debug=True)