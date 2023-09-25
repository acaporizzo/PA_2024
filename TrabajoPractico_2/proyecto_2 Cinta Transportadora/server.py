from flask import Flask, render_template, request, redirect, url_for
app = Flask("server")


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')