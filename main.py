from website import create_app

app = create_app()

if __name__ == '__main__':  #Only if we run this file,we are going to execute this line
    app.run(debug=True)     #Run the website app,with debug = TRue for every change made

    