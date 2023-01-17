from flask import Flask
from flask import render_template, redirect, url_for, request
from flask import jsonify
from flaskext.mysql import MySQL
from blockchain import Block, Blockchain

app = Flask(__name__)
appChain = Blockchain()

### MySQL configs
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '#Rocketman84'
app.config['MYSQL_DATABASE_DB'] = 'blockchain'
mysql.init_app(app)

### Home
@app.route('/', methods=['GET', 'POST'])
def HomeActionResult():
    '''
    Handles actions in home page.
    RENDER:
    Home Page
    '''

    if request.method == 'POST':
        # user chose a command
        requestAction = request.form
        if 'New Transaction' in requestAction:
            return redirect(url_for('Transaction'))
        
        elif 'Mine' in requestAction:
            return redirect(url_for('MineLoading'))

    return render_template("home.html")

### Transactions
@app.route('/transactions', methods=['POST', 'GET'])
def Transaction():
    '''
    Handles actions in transactions page.
    RENDER:
    Transactions Page
    '''

    if request.method == 'POST':
        requestAction = request.form
        # get transaction info from the request
        sender = requestAction['Sender']
        recipient = requestAction['Recipient']
        amount = float(requestAction['Amount'])

        # add the transaction to the blockchain
        appChain.NewTransaction(sender, recipient, amount)

        # insert into mySQL pending_transactions table
        # Connect to the database
        conn = mysql.connect()
        # Create a cursor
        curs = conn.cursor()
        curs.execute('''
            INSERT INTO pending_transactions (sender, recipient, amount) 
            VALUES (%s, %s, %s)''', (sender, recipient, amount))
        
        # save to db
        conn.commit()
        # Close the cursor and connection
        curs.close()
        conn.close()

        return redirect('/transactions')
    
    else:
        # show all pending transactions
        transactions = appChain.currentTransactions
        return render_template('transactions.html', transactions=transactions)
    

### Mining
@app.route('/mine', methods=['GET'])
def Mine():
    '''
    Performs mining for a block.
    :return: <dict> New block generated and its data.
    '''

    newBlock = appChain.Mine()
    jsonBlock = {
        'index': newBlock.index,
        'transactions': newBlock.transactions,
        'previousHash': newBlock.prevHash,
        'timestamp': newBlock.timestamp,
        'proof': newBlock.nonce,
        'difficulty': newBlock.difficulty
    }

    return jsonBlock

@app.route('/mining', methods=['GET'])
def MineLoading():
    #TODO: Show nonces being generate during mining process to show user mining is being done.
    '''
    RENDER:
    Loading screen for when mining is happening.
    '''
    return render_template('mining.html')

@app.route('/mining/completed', methods=['POST', 'GET'])
def MininingCompleted():
    '''
    Handles actions in mining completed page.
    Show information for mined block when mining is completed.
    '''
    if request.method == 'POST':
        # User wants to mine again
        requestAction = request.form

        if 'Mine' in requestAction:
            return redirect(url_for('MineLoading'))
    
    else:
        # Render new block mined.
        newBlock = appChain.LastBlock
        return render_template('miningCompleted.html', newBlock=newBlock)

if __name__ == '__main__':
    app.run(debug=True)