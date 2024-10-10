from flask import Flask, render_template, redirect, url_for, request, jsonify
from blockchain import Block, Blockchain

app = Flask(__name__)
appChain = Blockchain()

### Home
@app.route('/', methods=['GET', 'POST'])
def HomeActionResult():
    '''
    Handles actions in home page.
    RENDER:
    Home Page
    '''
    if request.method == 'POST':
        requestAction = request.form
        if 'New Transaction' in requestAction:
            return redirect(url_for('Transaction'))
        elif 'Mine' in requestAction:
            return redirect(url_for('MineLoading'))
    return render_template("home.html")

@app.route('/blockchain', methods=['GET'])
def ViewBlockchain():
    '''
    Displays the entire blockchain.
    '''
    blockchain = appChain.chain
    return render_template('blockchain.html', blockchain=blockchain)

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
        sender = requestAction['Sender']
        recipient = requestAction['Recipient']
        amount = float(requestAction['Amount'])

        # Add the transaction to the blockchain
        appChain.NewTransaction(sender, recipient, amount)
        return redirect('/transactions')
    else:
        # Show all pending transactions
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
    # Return JSON response
    return jsonify(jsonBlock)

@app.route('/mining', methods=['GET'])
def MineLoading():
    '''
    Undergoes mining process.
    RENDER:
    Loading screen for when mining is happening.
    '''
    return render_template('mining.html')

### Mining completed with block details
@app.route('/mining/completed', methods=['POST', 'GET'])
def MininingCompleted():
    '''
    Handles actions in mining completed page.
    Shows information for mined block, including transactions.
    '''
    if request.method == 'POST':
        requestAction = request.form
        if 'Mine' in requestAction:
            return redirect(url_for('MineLoading'))
    else:
        # Get the latest mined block
        newBlock = appChain.LastBlock

        # Render new block mined with transactions
        return render_template('miningCompleted.html', newBlock=newBlock)

if __name__ == '__main__':
    app.run(debug=True)
