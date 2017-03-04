from flask import Flask
from flask import render_template
from flask import request
import json
from operator import itemgetter
from random import randint


app = Flask("Flappy Bird")

class Leaderboard:
    def __init__(self):
        # scores contain tuples of (name, score)
        # ordered by score (max to min)
        self.scores = []
        self.capacity = 10 # maximum leaderboard capacity

    def submit_score(self, name, score):
        if (len(name) > 2 and (name, score) not in self.scores):
            self.scores.append((name, score)) # appends tuple to scores array
            self.scores = sorted(self.scores, key=itemgetter(1), reverse=True)
            if len(self.scores) > self.capacity:
                self.scores.pop(self.capacity-1) # removes last element

lb = Leaderboard()
names = ["Beyonce", "Adele", "Selena", "Taylor"]
for name in names:
    lb.submit_score(name, randint(0,100))

@app.route("/")
def home():
    return render_template("index.html", scores=lb.scores)
    
@app.route("/scores", methods={"POST"})
def scores():
    # extract data from request
    name = request.json["name"]
    score = request.json["score"]
    lb.submit_score(name, score)
    return json.dumps({"status":"OK", "scores":lb.scores})

if __name__ == "__main__":
    app.run(debug=True)

