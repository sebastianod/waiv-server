import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import json
from operator import itemgetter
import io
import base64  # to turn svg to string and later to json


# Initializing flask app
app = Flask(__name__)

# #enable CORS
CORS(app)

# This sets the backend to Agg and avoids any issues related to creating matplotlib figures in a non-interactive environment.
matplotlib.use('Agg')

# ======== wave creation ========== #


@app.route('/api/getwave', methods=['POST']) #use api route for any api related task
def my_function():
    # ------------receive values------------#
    values = request.get_json()  # convert data (request) in JSON to python dict

    # -----------extract values-----------#
    clientHeight, clientAmplitude, clientCrazyness, clientBackgroundColor, clientWaveColor = itemgetter(
        "height",
        "amplitude",
        "crazyness",
        "backgroundColor",
        "waveColor")(values)  # destructuring incoming data

    clientHeight = int(clientHeight)  # turn string to int
    clientCrazyness = int(clientCrazyness)
    clientAmplitude = float(clientAmplitude)  # turn string to float (decimals)

    # ------------Generate wave------------#

    # Domain
    x = np.linspace(0, 2*np.pi, 4000)

    # -----------Fourier Series----------#
    # the higher n, the quicker you see a pattern
    def fourierSeries(amplitude, domain, crazyness):
        y = 0
        for i in range(crazyness):
            an = np.random.rand()
            bn = np.random.rand()
            alpha = np.random.rand()*3
            beta = np.random.rand()*4
            y += an*np.cos(i*domain + alpha) + bn*np.sin(i*domain + beta)
        return amplitude*y

    # RANGES: height: 0-8, crazyness: 2-10 , amplitude: 0.1 - 0.5
    y = fourierSeries(clientAmplitude, x, clientCrazyness)

    # Above zero
    actualY = y - y.min()  # take the minimum negative value and add a height

    # Create a figure and axis
    fig, ax = plt.subplots()

    # set the size of the figure to 6 inches wide by 4 inches tall
    fig.set_size_inches(13, 4)

    # Fill the area underneath the curve with color
    ax.fill_between(
        x,
        0,
        actualY + clientHeight,
        where=actualY > 0,
        interpolate=True,
        color=clientWaveColor,
        alpha=1
    )

    # Fill the area above the curve with red
    # ax.fill_between(x, actualY.max()+5, actualY, where=actualY>0, interpolate=True, color='red', alpha=1)

    # set x and y limits of the plot
    ax.set_ylim(0.0, 15)  # maximum value of the function plus a constant
    ax.set_xlim(0.0, x[-1])  # from zero to the last value of the x array

    # Do not show axis
    ax.axis('off')

    # Set the background color of the fifure
    fig.set_facecolor(clientBackgroundColor)

    # Set the padding around the plot to zero
    fig.subplots_adjust(
        left=0,
        bottom=0,
        right=1,
        top=1
    )

    # save the plot, must include the color of the figure, no edge colors and no padding
    fig.savefig("test.svg", facecolor=fig.get_facecolor(),
                edgecolor='none', pad_inches=0)
    
    # close the figure to free up memory
    plt.close(fig)

    # ----------Encoding------------#

    # load the SVG file and encode it to base64 and then to string
    with open('test.svg', 'rb') as file:
        encoded_svg = base64.b64encode(file.read()).decode(
            'utf-8')  # convert bytes to str

    # create the response JSON data with the encoded SVG
    response_data = {'svg': encoded_svg}  # encoded_svg is in str

    # return the response as JSON
    return jsonify(response_data)  # jsonify is a flask wrapper


if __name__ == '__main__':
    app.run(debug=True)

# This code converts to base 64 which can be converted easily online back to an svg
# -----Convert svg to base64-----#

    # with open('test.svg', 'rb') as file:
    #     encoded_svg = base64.b64encode(file.read()) # svg->base64
