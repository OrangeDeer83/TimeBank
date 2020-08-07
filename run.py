from app import app
'''
@app.route('/')
def index():
    data = db.engine.execute("show databases").fetchall()
    print(data)
    #data = account.query.all()
    #for i in data:
    #    print(i.userID)
    return 'this is root'
'''
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)