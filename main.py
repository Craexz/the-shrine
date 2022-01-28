from flask import Flask, request, render_template
import random, base64

app = Flask(__name__)


def encode(text):
    text_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(text_bytes)
    encoded = base64_bytes.decode('ascii')
    return encoded


def decode(text):
    text_bytes = text.encode('ascii')
    decoded_bytes = base64.b64decode(text_bytes)
    decoded = decoded_bytes.decode('ascii')
    return decoded


@app.route('/')   
def start():
    return render_template('index.html')


@app.route('/load_report')
def load_report():
    return render_template('report.html')


@app.route('/send_report', methods=['POST'])
def send_report():
    report = request.form['report']
    reportfile = open('reports.txt', 'a')
    reportfile.write(report)
    reportfile.write('\n')
    return render_template('message.html', message="Sent report successfully!")


@app.route("/login")
def load_login():
    return render_template("login.html")


@app.route('/homepage', methods=['POST'])
def homepage():
    global username_
    username_ = request.form['username']
    password_ = request.form['password']
    usernamefile = open("src/usernames.txt", 'r')
    passwordfile = open('src/passwords.txt', 'r')
    currencyfile = open('src/currency.txt', 'r')
    passlist = passwordfile.read().splitlines()
    userlist = usernamefile.read().splitlines()
    usernames = []
    passwords = []

    for username in userlist:
        username = decode(username)
        usernames.append(username)

    for password in passlist:
        password = decode(password)
        passwords.append(password)

    try:  
        global usernameindex
        usernameindex = usernames.index(username_)
        usernameindex = int(usernameindex)
    except ValueError:
        return render_template("incorrectlogin.html")
    currencylist = []
    print(username_, password_)
    if username_ in usernames and password_ in passwords:
        currencylines = currencyfile.read().splitlines()
        for currency in currencylines:
            currencylist.append(currency)
        currency = currencylist[usernameindex]
        currency = decode(currency)
        global currency__ 
        currency__ = currency
        postlist = []

        postsfile = open('src/posts.txt', 'r')
        for post in postsfile.read().splitlines():
            postlist.append(post)
        try:
            title1 = postlist[0]
        except IndexError:
            return render_template('homepage.html', currency=currency)
        try:
            price1 = postlist[1]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1)
        try:
            description1 = postlist[2]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1)     
        try:
            title2 = postlist[5]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1)
        try:
            price2 = postlist[6]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1,
                                   title2=title2)
        try:
            description2 = postlist[7]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1,
                                   title2=title2,
                                   price2="Price: " + price2)
        try:
            title3 = postlist[10]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1,
                                   title2=title2,
                                   price2="Price: " + price2,
                                   description2="Description: " + description2)
        try:
            price3 = postlist[11]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1,
                                   title2=title2,
                                   price2="Price: " + price2,
                                   description2="Description: " + description2,
                                   title3=title3)
        try:
            description3 = postlist[12]
        except IndexError:
            return render_template('homepage.html',
                                   currency=currency,
                                   title1=title1,
                                   price1="Price: " + price1,
                                   description1="Description: " + description1,
                                   title2=title2,
                                   price2="Price: " + price2,
                                   description2="Description: " + description2,
                                   title3=title3,
                                   price3="Price: " + price3)

        return render_template('homepage.html',
                               currency=currency,
                               title1=title1,
                               price1="Price: " + price1,
                               description1="Description: " + description1,
                               title2=title2,
                               price2="Price: " + price2,
                               description2="Description: " + description2,
                               title3=title3,
                               price3="Price: " + price3,
                               description3="Description: " + description3)
    else:
        return render_template("incorrectlogin.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/post_signup', methods=['POST'])
def post_signup():
    username = request.form['username']
    password = request.form['password']
    if username == '' or password == '':
        return render_template("message.html",
                               message='Credentials not allowed, try again')
    passwordfile = open("src/passwords.txt", 'r')
    usernamefile = open('src/usernames.txt', 'r')

    password = encode(password)

    username = encode(username)

    passlist = passwordfile.read().splitlines()
    userlist = usernamefile.read().splitlines()

    if password in passlist and username in userlist:
        return render_template("accounttaken.html")
    else:
        passwordfile = open("src/passwords.txt", 'a')
        usernamefile = open('src/usernames.txt', 'a')
        currencyfile = open('src/currency.txt', 'a')
        starter_currency = '200'
        currency = encode(starter_currency)
        usernamefile.write(username)
        usernamefile.write('\n')
        passwordfile.write(password)
        passwordfile.write('\n')
        currencyfile.write(currency)
        currencyfile.write('\n')
        return render_template("login.html")


@app.route('/payment', methods=['POST'])
def payment():
    user = request.form['user']
    amount = request.form['amount']
    amount = int(amount)
    accounts = [] 
    currencylist = [] 

    user_encrypted = encode(user)
    local_user_encrypted = encode(username_)

    usernamefile = open("src/usernames.txt", 'r')
    currencyfile = open('src/currency.txt', 'r')
    for account in usernamefile.read().splitlines():
        accounts.append(account)
    local_user_index = accounts.index(local_user_encrypted)
    try:
        accountindex = accounts.index(user_encrypted)
    except ValueError:
        return render_template('message.html',
                               message='User "' + user + '"' +
                               ' does not exist')
    currencylines = currencyfile.read().splitlines()
    for currency in currencylines:
        currencylist.append(currency)
    current_currency = currencylist[accountindex]
    local_currency = currencylist[local_user_index]

    local_currency = decode(local_currency)

    amountint = int(amount)
    local_currency_int = int(local_currency)
    if amountint > local_currency_int:
        return render_template(
            'message.html',
            message='Payment amount higher than your current balance')
    current_currency = decode(current_currency)
    current_currency = int(current_currency)
    new_currency = amount + current_currency

    curr_bytes = repr(new_currency).encode('ascii')
    base64_currency_bytes = base64.b64encode(curr_bytes)
    new_currency = base64_currency_bytes.decode('ascii')

    def replace_line(file_name, line_num, text):
        with open(file_name, 'r') as file:
            data = file.read().splitlines()
            data[line_num] = text
        f = open(file_name, 'r+')
        f.truncate(0)
        with open(file_name, 'w') as file:
            for line in data:
                line = str(line)
                writethis = line, "\n"
                file.writelines(writethis)

    replace_line('src/currency.txt', accountindex, new_currency)  
    return render_template("payment.html", user=user, payment_amount=amount)


@app.route('/home')
def post_payment():
    return render_template("homepage.html", currency=currency__)


@app.route('/createpost', methods=['POST'])
def createpost():
    title = request.form['title']
    price = request.form['price']
    description = request.form['description']
    link = request.form['link']
    linelist = []
    postfile = open('src/posts.txt', 'r')
    for line in postfile.read().splitlines():
        linelist.append(line)
    if len(linelist) == 9 or len(linelist) > 9:
        return render_template('message.html',
                               message='Posts are already taken')
    postfile = open('src/posts.txt', 'a')   
    postfile.write(title)
    postfile.write('\n')
    postfile.write(price)
    postfile.write('\n')
    postfile.write(description)
    postfile.write('\n')
    postfile.write(link)
    postfile.write('\n')
    postfile.write(username_)
    postfile.write('\n')

    return render_template('relogin.html')


@app.route("/buyfirstpost")
def buyfirstpost():
    postfile = open('src/posts.txt', 'r')
    postlines = []
    for line in postfile.read().splitlines():
        postlines.append(line)

    amount = postlines[1]
    poster = postlines[4]
    amount = int(amount)
    accounts = []   
    currencylist = []

    poster_encrypted = encode(poster)

    local_user_encrypted = encode(username_)

    usernamefile = open("src/usernames.txt", 'r')
    currencyfile = open('src/currency.txt', 'r')
    for account in usernamefile.read().splitlines():
        accounts.append(account)
    local_user_index = accounts.index(local_user_encrypted)
    accountindex = accounts.index(poster_encrypted)
    currencylines = currencyfile.read().splitlines()
    for currency in currencylines:
        currencylist.append(currency)
    current_currency = currencylist[accountindex]
    local_currency = currencylist[local_user_index]

    local_currency = decode(local_currency)

    amountint = int(amount)
    local_currency_int = int(local_currency)
    if amountint > local_currency_int:
        return render_template(
            'message.html',     
            message='Payment amount higher than your current balance')

    current_currency = decode(current_currency)

    current_currency = int(current_currency)
    new_currency = amount + current_currency

    curr_bytes = repr(new_currency).encode('ascii')
    base64_currency_bytes = base64.b64encode(curr_bytes)
    new_currency = base64_currency_bytes.decode('ascii')

    def replace_line(file_name, line_num, text):
        with open(file_name, 'r') as file:
            data = file.read().splitlines()
            data[line_num] = text
        f = open(file_name, 'r+')
        f.truncate(0)
        with open(file_name, 'w') as file:
            for line in data:
                line = str(line)
                writethis = line, "\n"
                file.writelines(writethis)

    replace_line('src/currency.txt', accountindex, new_currency)
       
    currencys = []
    currencyfile = open('src/currency.txt', 'r')
    for currency in currencyfile.read().splitlines():
        currencys.append(currency)
    currency_index = usernameindex
    amount = int(amount)    
    deducted_currency = (local_currency_int) - amount

    dcny_bytes = repr(deducted_currency).encode('ascii')
    base64_dcny = base64.b64encode(dcny_bytes)
    deducted_currency = base64_dcny.decode('ascii')

    replace_line('src/currency.txt', currency_index, deducted_currency)
    link = postlines[3]
    name = postlines[0]
    if type(amount) == int:
        amount = str(amount)

    message = ("Successfully bought the product '" + name + "' with " +
               amount + " tokens! " + "Link to post: " + link)
    return render_template("bought_post.html", message=message)


@app.route("/buysecondpost")
def buysecondpost():
    postfile = open('src/posts.txt', 'r')
    postlines = []
    for line in postfile.read().splitlines():
        postlines.append(line)

    amount = postlines[6]
    poster = postlines[9]
    amount = int(amount)
    accounts = []
    currencylist = []

    poster_encrypted = encode(poster)

    local_user_encrypted = encode(username_)

    usernamefile = open("src/usernames.txt", 'r')
    currencyfile = open('src/currency.txt', 'r')
    for account in usernamefile.read().splitlines():
        accounts.append(account)  
    local_user_index = accounts.index(local_user_encrypted)
    accountindex = accounts.index(poster_encrypted)
    currencylines = currencyfile.read().splitlines()
    for currency in currencylines:
        currencylist.append(currency)
    current_currency = currencylist[accountindex]
    local_currency = currencylist[local_user_index]

    local_currency = decode(local_currency)
    amountint = int(amount)
    local_currency_int = int(local_currency)
    if amountint > local_currency_int:
        return render_template(
            'message.html',
            message='Payment amount higher than your current balance')

    current_currency = decode(current_currency)
    current_currency = int(current_currency)
    new_currency = amount + current_currency

    curr_bytes = repr(new_currency).encode('ascii')
    base64_currency_bytes = base64.b64encode(curr_bytes)
    new_currency = base64_currency_bytes.decode('ascii')

    def replace_line(file_name, line_num, text):
        with open(file_name, 'r') as file:
            data = file.read().splitlines()
            data[line_num] = text
        f = open(file_name, 'r+')
        f.truncate(0)
        with open(file_name, 'w') as file:
            for line in data:
                line = str(line)
                writethis = line, "\n"
                file.writelines(writethis)

    replace_line('src/currency.txt', accountindex, new_currency)

    currencys = []
    currencyfile = open('src/currency.txt', 'r')
    for currency in currencyfile.read().splitlines():
        currencys.append(currency)
    currency_index = usernameindex
    amount = int(amount)
    deducted_currency = (local_currency_int) - amount

    dcny_bytes = repr(deducted_currency).encode('ascii')
    base64_dcny = base64.b64encode(dcny_bytes)
    deducted_currency = base64_dcny.decode('ascii')

    replace_line('src/currency.txt', currency_index, deducted_currency)
    name = postlines[7]
    link = postlines[10]
    message = ("Successfully bought " + name + " with " + str(amount) +
               " tokens! " + "Link to post: " + link)
    return render_template("bought_post.html", message=message)


@app.route("/buythirdpost") 
def buythirdpost():
    postfile = open('src/posts.txt', 'r')
    postlines = []
    for line in postfile.read().splitlines():
        postlines.append(line)

    amount = postlines[11]
    poster = postlines[14]
    amount = int(amount)
    accounts = []
    currencylist = []

    poster_encrypted = encode(poster)

    local_user_encrypted = encode(username_)

    usernamefile = open("src/usernames.txt", 'r')
    currencyfile = open('src/currency.txt', 'r')
    for account in usernamefile.read().splitlines():
        accounts.append(account)
    local_user_index = accounts.index(local_user_encrypted)
    accountindex = accounts.index(poster_encrypted)
    currencylines = currencyfile.read().splitlines()
    for currency in currencylines:
        currencylist.append(currency)
    current_currency = currencylist[accountindex]
    local_currency = currencylist[local_user_index]

    local_currency = decode(local_currency)
    amountint = int(amount)
    local_currency_int = int(local_currency)
    if amountint > local_currency_int:
        return render_template(
            'message.html',
            message='Payment amount higher than your current balance')

    current_currency = decode(current_currency)
    current_currency = int(current_currency)
    new_currency = amount + current_currency

    curr_bytes = repr(new_currency).encode('ascii')
    base64_currency_bytes = base64.b64encode(curr_bytes)
    new_currency = base64_currency_bytes.decode('ascii')

    def replace_line(file_name, line_num, text):
        with open(file_name, 'r') as file:
            data = file.read().splitlines()
            data[line_num] = text
        f = open(file_name, 'r+')
        f.truncate(0)
        with open(file_name, 'w') as file:
            for line in data:
                line = str(line)
                writethis = line, "\n"
                file.writelines(writethis)

    replace_line('src/currency.txt', accountindex, new_currency)

    currencys = []    
    currencyfile = open('src/currency.txt', 'r')
    for currency in currencyfile.read().splitlines():
        currencys.append(currency)
    currency_index = usernameindex
    amount = int(amount)
    deducted_currency = (local_currency_int) - amount

    dcny_bytes = repr(deducted_currency).encode('ascii')
    base64_dcny = base64.b64encode(dcny_bytes)
    deducted_currency = base64_dcny.decode('ascii')

    replace_line('src/currency.txt', currency_index, deducted_currency)
    name = postlines[12]
    link = postlines[15]
    message = ("Successfully bought " + name + " with " + str(amount) +
               " tokens! " + "Link to post: " + link)
    return render_template("bought_post.html", message=message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
