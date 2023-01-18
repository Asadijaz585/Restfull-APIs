from flask import Flask,render_template, request, json
from flask_mysqldb import MySQL


app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scraping'
 
mysql = MySQL(app)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
#  https://rogerbinns.github.io/apsw/cursor.html

@app.route('/<int:id>', methods = ['GET'])
def GET(id):
    request.method == 'GET'
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM `insta_record` WHERE id={}'.format(id))
    result = cursor.fetchone()
    print(result)
    fetchedData = json.dumps(result)
    mysql.connection.commit()
    cursor.close()
    return fetchedData
     

@app.route('/', methods = ['POST'])
def POST():
    if request.method == 'POST':
        req_data = request.get_json()
        name = req_data['name']
        posts = req_data['posts']
        followers = req_data['followers']
        following = req_data['following']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM insta_record")
        cursor.execute(''' INSERT IGNORE INTO insta_record (name, posts, followers, following) VALUES(%s, %s, %s, %s)''',(name, posts, followers, following))
        mysql.connection.commit()
    return '''name: {}.
              posts: {}.
              followers: {}.
              following: {}'''.format(name, posts, followers, following)

@app.route('/<int:id>', methods = ['PUT'])
def UPDATE(id):
    if request.method == 'PUT':
        req_data = request.get_json()
        name = req_data['name']
        posts = req_data['posts']
        followers = req_data['followers']
        following = req_data['following']
        cursor = mysql.connection.cursor()
        cursor.execute(''' UPDATE insta_record SET name = %s, posts = %s, followers = %s, following = %s WHERE id = %s''',(name, posts, followers, following, id))
        cursor.execute("SELECT * FROM insta_record")
        mysql.connection.commit()
    return '''name: {}.
              posts: {}.
              followers: {}.
              following: {}'''.format(name, posts, followers, following)

@app.route('/<int:id>', methods = ['DELETE'])
def DELETE(id):
    if request.method == 'DELETE':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM insta_record")
        cursor.execute(''' DELETE FROM insta_record WHERE id = %s''',{id})
        mysql.connection.commit()
    return 'DELETED'

if __name__ == "__main__":
    app.run(host='localhost', port=5000)