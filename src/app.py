from flask import Flask, render_template, request, Response
import pandas as pd
import numpy as np
import io
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, date, timedelta
from pandas_datareader import data as web
from service import ROC, get_stock, buy_sell
matplotlib.use('Agg')

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def stocks():

    title = request.args['title']
    start_date = request.args['start_date']
    end_date = request.args['end_date']

    df = pd.DataFrame(get_stock(title, start_date, end_date))
    df['ROC20'] = ROC(df['Close'], 20)
    df['SMAROC20'] = df['ROC20'].rolling(window=10).mean()
    df['ROC50'] = ROC(df['Close'], 50)
    df['SMAROC50'] = df['ROC50'].rolling(window=10).mean()
    df['ROC100'] = ROC(df['Close'], 100)
    df['SMAROC100'] = df['ROC100'].rolling(window=10).mean()
    df['ROC200'] = ROC(df['Close'], 200)
    df['SMAROC200'] = df['ROC200'].rolling(window=10).mean()

    buy_sellValue = buy_sell(df)
    df['Buy_Signal_Price'] = buy_sellValue[0]
    df['Sell_Signal_Price'] = buy_sellValue[1]
    dateDelta = date.today() - timedelta(days=3)   
    timeFrame = df[df.index > dateDelta.strftime("%m-%d-%Y")]

    if not timeFrame['Buy_Signal_Price'].isnull().any().any():
        return 'Buy'
    
    elif not timeFrame['Sell_Signal_Price'].isnull().any().any():
        return 'Sell'
    
    else:
        return 'Flat'






    return 'hello'


def create_title(df, title):
    fig, ax = plt.subplot(figsize=(20, 10))
    ax.plot(df['Close'], label=title)
    ax.title('Close Price')
    ax.xlabel('One year windows')
    ax.ylabel('Price in euro')
    fig.legend(loc='upper left')
    return fig

def create_ROC_subplots(df):
    fig, (ax1, ax2,ax3,ax4) = plt.subplots(4,figsize=(20, 10))
    fig.suptitle('ROC and SMA')

    ax1.plot(df['ROC20'], label='ROC20')
    ax1.plot(df['SMAROC20'], label='SMAROC20')
    ax2.plot(df['ROC50'], label='ROC50')
    ax2.plot(df['SMAROC50'], label='SMAROC50')
    ax3.plot(df['ROC100'], label='ROC100')
    ax3.plot(df['SMAROC100'], label='SMAROC100')
    ax4.plot(df['ROC200'], label='ROC200')
    ax4.plot(df['SMAROC200'], label='SMAROC200')
    fig.legend(loc='upper left')
    return fig

if __name__ == '__main__':
    app.run()