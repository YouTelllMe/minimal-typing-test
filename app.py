import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
import random
import base64
import time

app = Flask(__name__)



CORS(app)

class Hello: 
    typedData = {}

    @staticmethod
    def time_for_letter(data):
        times = []
        word = []
        for i in data:
            if len(data[i]) > 0:
                word.append(i)
            elif len(data[i]) == 0:
                if len(word) > 0:
                    times.append(word)
                    word = []
        
        times.append(word)

        for i in times:
            c = 1
            while c < len(i):
                if float(i[c]) < float(i[c-1]):
                    i.pop(c-1)
                c += 1

        result = {}
        for x in times:
            y = 1
            while y < len(x):
                if len(data[x[y]]) == 2:
                    if data[x[y]][0] == data[x[y-1]][-1]:
                        letters = data[x[y]][-1]
                        time = float(x[y]) - float(x[y-1])
                        if letters in result:
                            result[letters].append(time)
                        else:
                            result[letters] = [time]
                y += 1

        for i in result:
            if len(result[i]) > 1:
                result[i] = sum(result[i]) / len(result[i])
                result[i] = float("%0.3f" % result[i])
            else:
                result[i] = float("%0.3f" % result[i][0])

        return result
    
    @staticmethod
    def plotBarGraph(data):
        data2 = dict(sorted(data.items(), key=lambda item: item[1]))

        COLOR = 'white'
        ORANGE = '#ffe7c7'
        #(255,231,199)
        plt.rcParams['text.color'] = COLOR
        plt.rcParams['axes.labelcolor'] = COLOR
        plt.rcParams['xtick.color'] = COLOR
        plt.rcParams['ytick.color'] = COLOR
        
        fig, ax = plt.subplots()
        plt.bar(range(len(data2)), list(data2.values()), align='center',color=(ORANGE))
        plt.xticks(range(len(data2)), list(data2.keys()))       

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLOR)
        ax.spines['bottom'].set_color(COLOR)
        plt.xlabel("Character")
        plt.ylabel("Time(s)")
        plt.title("Average Time (s) vs. Character Press")


        plt.savefig('static/media/results.png',transparent=True) 

        with open ('static/media/results.png', 'rb') as results:
            return (base64.b64encode(results.read()))


    @staticmethod
    def random_passage():
        f = open('sentences.txt', 'r')
        l = f.readlines()
        choice = random.randint(0, len(l) - 1)
        f.close()    
        return(l[choice])


@app.route('/API',methods=['POST', 'GET'])
@cross_origin()
def processjson():
    if request.method == 'POST':
            Hello.typedData = request.get_json()
            return jsonify({'post': 'success!'})
    else:
        processedData = Hello.time_for_letter(Hello.typedData)
        x = Hello.plotBarGraph(processedData)
        return x

@app.route('/API/sample', methods=['GET'])
@cross_origin()
def sample():
    return jsonify({"sample":Hello.random_passage().rstrip('\n')})

@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()