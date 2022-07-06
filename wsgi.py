from shoppingApp import create_app, db


app = create_app()
db.create_all(app=app)

app.run(debug=False, port=5020)
