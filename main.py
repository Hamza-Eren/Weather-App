from tkinter import *
from PIL import ImageTk,Image
import requests
from bs4 import BeautifulSoup as bs
import json

url = "http://api.openweathermap.org/data/2.5/weather"
api_key = "API_KEY"
iconUrl = "http://openweathermap.org/img/wn/{}@2x.png"
genisUrl = "https://www.havadurumu15gunluk.xyz/havadurumu/854/{}-hava-durumu-15-gunluk.html"

def regulation():
    if iconLabel.winfo_x() != 20:
        xi = iconLabel.winfo_x() + 1
        xt = tempLabel.winfo_x() - 1
        xc = conditionLabel.winfo_x() - 1
        yl = locationLabel.winfo_y() - 1

        iconLabel.place(x=xi, y=70, height=100, width=100)
        tempLabel.place(x=xt, y=120, height=50, width=156)
        conditionLabel.place(x=xc, y=70, height=50, width=156)
        locationLabel.place(x=40, y=yl, height=20, width=220)
        
        app.after(5, regulation)

def control(*args):
    error.place_forget()
    if iconLabel.winfo_x() != -150:
        xi = iconLabel.winfo_x() - 1
        xt = tempLabel.winfo_x() + 1
        xc = conditionLabel.winfo_x() + 1
        yl = locationLabel.winfo_y() + 1

        iconLabel.place(x=xi, y=70, height=100, width=100)
        tempLabel.place(x=xt, y=120, height=50, width=156)
        conditionLabel.place(x=xc, y=70, height=50, width=156)
        locationLabel.place(x=40, y=yl, height=20, width=220)
        
        app.after(5, control)

    if iconLabel.winfo_x() == -150:
        main()
    
def getWeather(sehir):
    params = {'q':sehir.upper().capitalize(), 'appid':api_key, 'lang':'tr'}
    data = requests.get(url,params=params).json()
    if data and data['cod'] == 200:
        sehir = data['name'].capitalize()
        ulke = data['sys']['country']
        sicaklik = int(data['main']['temp'] - 273)
        icon = data['weather'][0]['icon']
        durum = data['weather'][0]['description'].capitalize()
        if len(durum) > 24:
            durum = durum[:22] + '...'
        return (sehir, ulke, sicaklik, icon, durum)
    else:
        error.place(x=20, y=70, width=260, height=140)
    
def main():
    global serviceURL
    sehir = sehirGirme.get()
    if sehir:
        weather = getWeather(sehir)
    else:
        r = requests.get(serviceURL)
        y = json.loads(r.text)
        weather = getWeather(y["region_name"])
    if weather:
        locationLabel['text'] = '{},{}'.format(weather[0],weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        conditionLabel['text'] = '{}'.format(weather[4])
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[3]),stream=True).raw))
        iconLabel.configure(image = icon)
        iconLabel.image = icon
        regulation()

        
app = Tk()
app.iconbitmap('images/icon.ico')
app.title('Hava Durumu')
app.geometry('306x230')
app.resizable(0,0)

sehirGirme = Entry(app)
sehirGirme.bind('<Return>', control)
sehirGirme.place(x=40, y=20, width=195, height=20)
sehirGirme.focus()

p1 = PhotoImage(file = "images/buyutec.png")
search_btn = Button(app, image=p1, borderwidth=0, command=control)
search_btn.place(x=240, y=17, width=26, height=26)

iconLabel = Label(app)
iconLabel.place(x=-150, y=70, width=100, height=100)

locationLabel = Label(app, font=('Arial',15))
locationLabel.place(x=40, y=360, width=220, height=20)

tempLabel = Label(app, font=('Arial',30,'bold'))
tempLabel.place(x=306, y=120, width=156, height=50)

conditionLabel = Label(app, font=('Arial',12))
conditionLabel.place(x=306, y=70, width=156, height=50)

p2 = PhotoImage(file = "images/error.png")
error = Label(app, image=p2)

app.mainloop()
