import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
from mypjt.settings import BASE_DIR
import base64


def problem1(request):
    
    df = pd.read_csv(BASE_DIR/'austin_weather.csv')
    df_html = df.to_html(classes='table table-bordered table-striped')
    context = {
        'df_html' : df_html
    }
    return render(request, 'weathers/problem1.html', context)


def problem2(request):
    df = pd.read_csv(BASE_DIR/'austin_weather.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    x = df['Date']
    y1 = df['TempHighF']
    y2 = df['TempAvgF']
    y3 = df['TempLowF']

    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.plot(x, y1, label='High Temperature', color='blue')
    plt.plot(x, y2, label='Avg Temperature', color='orange')
    plt.plot(x, y3, label='Low Temperature', color='green')

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.grid(True)
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'chart_image':f'data:image/png;base64,{image_base64}'
    }

    return render(request, 'weathers/problem2.html', context)


def problem3(request):
    df = pd.read_csv(BASE_DIR/'austin_weather.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['TempHighF'] = pd.to_numeric(df['TempHighF'], errors='coerce')
    x = df.resample('M', on='Date')['Date'].max()
    y1 = df.resample('M', on='Date')['TempHighF'].mean()
    y2 = df.resample('M', on='Date')['TempAvgF'].mean()
    y3 = df.resample('M', on='Date')['TempLowF'].mean()

    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.plot(x, y1, label='High Temperature', color='blue')
    plt.plot(x, y2, label='Avg Temperature', color='orange')
    plt.plot(x, y3, label='Low Temperature', color='green')

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.grid(True)
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'chart_image':f'data:image/png;base64,{image_base64}'
    }

    return render(request, 'weathers/problem3.html', context)


def problem4(request):
    df = pd.read_csv(BASE_DIR/'austin_weather.csv')
    # df['Events'].fillna('No Events', inplace=True)

    counts = {}
    for event_list in df['Events']:
        events = event_list.split(',')
        for event in events:
            event = event.strip()
            counts[event] = counts.get(event, 0) + 1

    if '' in counts:
        counts['No Events'] = counts['']
        del counts['']

    sorted_events = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    events, cnts = zip(*sorted_events)
    
 
    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.bar(events,cnts)

    plt.title('Events Counts')
    plt.xlabel('Events')
    plt.ylabel('Count')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    context = {
        'chart_image':f'data:image/png;base64,{image_base64}'
    }

    return render(request, 'weathers/problem4.html', context)
