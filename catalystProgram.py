from bokeh.plotting import figure, show
from bokeh.io import curdoc
import numpy
global waterFile, airFile
waterFile = open("waterData.txt", "r")
airFile = open("airPollutionData.txt", "r")

def main():
    data = makeData()
    data = cleanData(data)
    makeGraph(data)

def makeGraph(dict):
    #sorting data
    airVals = []
    waterVals = []
    countries = []
    for key in dict:
        countries.append(key)
        airVals.append(int(dict[key][0]))
        waterVals.append(int(dict[key][1]))


    plot = figure(width = 600, height = 600)
    plot.circle(airVals, waterVals, size = 6, color = (167, 156, 69))

    #trendline
    mean_x = numpy.mean(airVals)
    mean_y = numpy.mean(waterVals)
    num = 0
    denom = 0

    for i in range(len(airVals)):
        num += (airVals[i] - mean_x) * (waterVals[i] - mean_y)
        denom += (airVals[i] - mean_x) ** 2

    m = num / denom
    c = mean_y - (m * mean_x)
    x = numpy.linspace(10, 300, 1000)
    plot.line(x, c + m * x)

    #customs
    plot.x_range.flipped = True
    plot.xaxis.axis_label = "Deaths Attributed to Air Pollution [Per 100k]"

    plot.yaxis.axis_label = "Population Accessing Water Filtration [%]"

    curdoc().theme = "dark_minimal"

    show(plot)


def cleanData(dict):
    remove = []
    for key in dict:
        if len(dict[key]) < 2:
            remove.append(key)

    for i in range(len(remove)):
        del dict[remove[i]]

    remove = []
    for key in dict:
        if dict[key][0] == '' or dict[key][1] == '':
            remove.append(key)

    for i in range(len(remove)):
        del dict[remove[i]]

    return dict



def makeData():
    global airFile, waterFile
    data = {}

    for line in airFile.readlines():
        if "Total" in line:
            line = line[line.index("\"") + 1: len(line)]

            l = line
            for i in range(5):
                l = l[l.index(",") + 1 : len(l)]
            l = l[1 : l.index(",")]

            data[line[0 : line.index("\"")]] = []
            data[line[0 : line.index("\"")]].append(l[0 : l.index(" ")])
    
    i = 0
    for line in waterFile.readlines():
        if i > 2:
            line = line[line.index("\"") : len(line)]

            l = line
            for i in range(13):
                l = l[l.index(",") + 1 : len(l)]
            l = l[1 : l.index(",") - 1]

            name = line[1 : line.index(",") - 1]
            if name in data:
                data[name].append(l)
   
        i += 1

    return data #will be a dictionary. each key will have an array associated as the value. 
                #the first index of the array will be the air, the second will be the water


if __name__ == "__main__":
    main()
