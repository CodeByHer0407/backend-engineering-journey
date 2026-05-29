### Building URL dynamically
## Variable Rule
### Jinja 2 template Engine

'''
{{  }}  expressions to print output in html 
{%...%} conditions, for loops
{#...#} this is for comments
'''


from flask import Flask, render_template, request

'''
It creates an instance of the Flask class,
which will be your WSGI (Web server gateway interface) application.
'''

### WSGI Application
app = Flask(__name__)

@app.route("/")
def welcome():
    return "<html><h1>Welcome to this Flask course. Happy learning!!</h1></html>"


@app.route("/index", methods = ["GET"])
def intro():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/submit", methods = ['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        return f'Hello {name}!'
    return render_template("form.html")


@app.route("/success/<int:score>")
def success(score):
    res = ""
    if score >= 50:
        res = "PASSED"
    else:
        res = "FAILED"

    return render_template('result.html', results=res)




@app.route("/successres/<int:score>")
def successres(score):
    res = ""
    if score >= 50:
        res = "PASSED"
    else:
        res = "FAILED"

    exp = {'score': score, 'res': res}

    return render_template('result1.html', results=exp)



if __name__ == "__main__":
    app.run(debug=True)