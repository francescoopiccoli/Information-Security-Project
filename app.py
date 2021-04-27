from website import create_app

app = create_app()

#only run the app (and start the webserver if we are running main file, not if this is file is imported in some other file)
if __name__ == '__main__':
    app.run(debug=True)     #debug=true -> everytime we make a change to the python code, manually rerun the web server to view changes


#to let a user add a post or comment or see his profile, he obviously neesds
# to be logged, to impose this constraint we use the decorator @login_required 