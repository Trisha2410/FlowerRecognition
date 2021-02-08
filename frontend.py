from googlesearch import search
import re
import requests
from tkinter import *
import requests
from tkinter import filedialog, Label, Tk
from PIL import Image, ImageTk
import cv2
import tensorflow.keras as keras
import numpy as np
from bs4 import BeautifulSoup

def scientificprint():
    #     scname = re.compile(r'<td>Genus:\n</td>\n<td><a class="mw-selflink selflink"><i>(.*?)<')
    scname = re.compile(r'<td>Genus:\n</td>\n<td><a href=\".*?\" title=\".*?\"><i>(.*?)<')
    a = scname.findall(html_content)
    return a[0]


def famnameprint():
    familyname = re.compile(r'<td>Family:\n</td>\n<td><a href=\".*?\" title=\".*?\">(.*?)<')
    b = familyname.findall(html_content)
    return b[0]


def kingdomprint():
    kingdom = re.compile(r'<td>Kingdom:\n</td>\n<td><a href=\".*?\" title=\".*?\">(.*?)<')
    c = kingdom.findall(html_content)
    return c[0]


def ordername():
    ordername = re.compile(r'<td>Order:\n</td>\n<td><a href=\".*?\" title=\".*?\">(.*?)<')
    d = ordername.findall(html_content)
    return d[0]

def flowerDescription(flower):
    url = "https://www.google.com/search?q=what+is+special+about+{}+flower".format(flower)
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    a = soup.find("div", {"class": "BNeawe s3v9rd AP7Wnd"})
    a = str(a)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', a)
    print("Description :\n",cleantext)
    return cleantext

def flowerMeaning(flower):

    url = "https://www.google.com/search?q=meaning+of+{}+flower".format(flower)
    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')
    a = soup.find("div", {"class": "BNeawe s3v9rd AP7Wnd"})
    a = str(a)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', a)
    print("Meaning :\n",cleantext)
    return cleantext


def flowerDictionary(flower):
    flower_dict = {'Bluebell': 'https://en.wikipedia.org/wiki/Mertensia_virginica',
                   'Buttercup': 'https://en.wikipedia.org/wiki/Ranunculus_repens',
                   'Colt Foot': 'https://en.wikipedia.org/wiki/Petasites_frigidus',
                   'Cowslip': 'https://en.wikipedia.org/wiki/Primula_veris#:~:text=Primula%20veris%2C%20the%20cowslip%2C%20common,in%20the%20primrose%20family%20Primulaceae.',
                   'Crocus': 'https://en.wikipedia.org/wiki/Crocus_sativus',
                   'Daffodil': 'https://en.wikipedia.org/wiki/Narcissus_pseudonarcissus',
                   'Daisy': 'https://en.wikipedia.org/wiki/Bellis_perennis',
                   'Dandellion': 'https://en.wikipedia.org/wiki/Taraxacum_officinale',
                   'Fritillary': 'https://en.wikipedia.org/wiki/Fritillaria_imperialis',
                   'Iris': 'https://en.wikipedia.org/wiki/Iris_versicolor',
                   'Lily Valley': 'https://en.wikipedia.org/wiki/Lily_of_the_valley#:~:text=Lily%20of%20the%20valley%2C%20Convallaria,Hemisphere%20in%20Asia%20and%20Europe.',
                   'Pansy': 'https://en.wikipedia.org/wiki/Viola_tricolor',
                   'Snowdrop': 'https://en.wikipedia.org/wiki/Galanthus_nivalis',
                   'Sunflower': 'https://en.wikipedia.org/wiki/Helianthus_annuus',
                   'Tiger Lily': 'https://en.wikipedia.org/wiki/Lilium_lancifolium',
                   'Tulips': 'https://en.wikipedia.org/wiki/Tulipa_sylvestris',
                   'Windflower': 'https://en.wikipedia.org/wiki/Anemone_blanda'}
    url=flower_dict[flower]
    return url

def browse():
    filename = filedialog.askopenfilename(initialdir="/",
                                          filetype=(("jpeg", "*.jpg"), ("PNG", "*.png"), ("All Files", "*.*")))
    img = Image.open(filename)
    # Below manipulation is for the display in the GUI
    wd, ht = img.size
    print(f" original width {wd}, original height {ht}")
    new_height = int(400 * ht / wd)
    new_width = int(400 * wd / ht)
    img_display = img.resize((new_width, new_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img_display)
    label_image = Label(image_load_frame, image=photo, bg='black')
    label_image.image = photo
    label_image.place(relheight=1, relwidth=1)

    #model and function execution
    #folders = ['Cowslip', 'Pansy', 'Lily Valley', 'Buttercup', 'Bluebell', 'Snowdrop', 'Fritillary', 'Tulips',
               # 'Windflower', 'Iris', 'Tiger Lily', 'Colt Foot', 'Dandellion', 'Daisy', 'Daffodil', 'Crocus',
               # 'Sunflower']
    folders=['Fritillary','Cowslip','Iris','Daffodil','Pansy','Dandellion','Lily Valley','Buttercup','Tulips','Bluebell','Snowdrop','Tiger Lily','Daisy','Windflower','Crocus','Colt Foot','Sunflower']
    model = keras.models.load_model("loss_27_accuracy_90_valloss_37_val_accuracy_87.h5")

    size=60,60
    img_array = cv2.imread((filename))
    new_array = cv2.resize(img_array, size)
    flower_train = np.array(new_array/ 255.0)
    #flower_train = flower_train / 255.0
    print(flower_train.shape)
    X = flower_train
    X = X[np.newaxis, ...]
    print(X.shape)
    prediction = model.predict(X)
    probabitlity=[]
    for ind,prob in enumerate(prediction[0]):
        print(f"For index {ind} the probability is {prob*100}")
        probabitlity.append(prob*100)
        max_prob=max(probabitlity)
    print("Maximum Probability",max_prob)
    if max_prob >= 85:
        predicted_index = np.argmax(prediction)
        print(f"predicted index:\t{predicted_index}")
        global flower_namePredicted
        flower_namePredicted = folders[predicted_index]
        print(f"Predicted Flower:\t{flower_namePredicted}")
        global html_content
        url = flowerDictionary(flower_namePredicted)
        print("url",url)
        html_content = requests.get(url).text
        commonNameResult_labl.config(text=flower_namePredicted,font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0")

        scientificResult=scientificprint()
        print("scientificResult_labl",scientificResult)
        scientificResult_labl.config(text=scientificResult,font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0")

        familyResult=famnameprint()
        print("familyResult_labl",familyResult)
        familyResult_labl.config(text=familyResult,font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0")

        kingdomResult=kingdomprint()
        print("kingdomResult_labl", kingdomResult)
        kingdomResult_labl.config(text=kingdomResult,font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0")

        orderResult=ordername()
        print("orderResult_labl", orderResult)
        orderResult_labl.config(text=orderResult,font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0")

        description_txt.config(state=NORMAL)
        description=flowerDescription(flower_namePredicted)
        description_txt.delete("1.0","end")
        print("description_txt", description)
        description_txt.insert(INSERT,description)

        meaning_txt.config(state=NORMAL)
        meaning=flowerMeaning(flower_namePredicted)
        meaning_txt.delete("1.0", "end")
        print("meaning_txt", meaning)
        meaning_txt.insert(INSERT,meaning)
    else:
        flower_not_found="Information not available"
        description_na="""Unfortunately, we are unable to identify the flower. Please upload a clear image.
        *Note: We currently support below given flowers.
                Fritillary, Cowslip, Iris, Daffodil, Pansy, Dandellion, Lily Valley,
                Buttercup, Tulips, Bluebell, Snowdrop, Tiger Lily, Daisy, Windflower,
                Crocus, Colt Foot, Sunflower
        """
        commonNameResult_labl.config(text=flower_not_found,font=("Script MT Bold",12), fg="red")
        scientificResult_labl.config(text=flower_not_found,font=("Script MT Bold",12), fg="red")
        familyResult_labl.config(text=flower_not_found,font=("Script MT Bold",12), fg="red")
        kingdomResult_labl.config(text=flower_not_found,font=("Script MT Bold",12), fg="red")
        orderResult_labl.config(text=flower_not_found,font=("Script MT Bold",12), fg="red")
        description_txt.config(state=NORMAL)
        description_txt.delete("1.0", "end")
        description_txt.insert(INSERT, description_na)
        meaning_txt.config(state=NORMAL)
        meaning_txt.delete("1.0", "end")
        meaning_txt.insert(INSERT,"Sorry, Information not available")


root = Tk()
root.title("FlowerPedia")
root.geometry("1000x800+10+10")
root.resizable(width=FALSE, height=FALSE)

bg_image=ImageTk.PhotoImage(Image.open("background1.jpg"))
Label(root,image=bg_image).place(relwidth=1,relheight=1)

image_quote = ImageTk.PhotoImage(Image.open("Flower_Quote1.jpg"))
image_quote_frame = Frame(root)
image_quote_frame.place(x=1,relwidth=1,relheight=0.15)
image_quote_lable =Label(image_quote_frame,image=image_quote)
image_quote_lable.place(relwidth=1,relheight=1)

image_load_frame= Frame(root,bg="#FFFFF0",relief='sunken',bd=2)
image_load_frame.place(x=5,y=110,height=350,width=350)
img = Image.open("sunflower.jpg")
default_photo = ImageTk.PhotoImage(img)
default_label_image = Label(image_load_frame, image=default_photo, bg='black')
default_label_image.image = default_photo
default_label_image.place(relheight=1, relwidth=1)

BrowseButton = Button(root, font=("Lucida Calligraphy", 16, 'bold'), text="Browse", width="6", height=5,
                        bd=6,bg="#0aacf7", fg='#FFFFF0',command=browse)
BrowseButton.place(x=95, y=445, width=160,height=49)


sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=170,height=5,width=30)

commonName_labl=Label(root, text="Common Name",bd=2, height=1, width=12, font=("Script MT Bold",18), fg="#FFFFF0",bg="#0aacf7",relief='groove')
commonName_labl.place(x=450,y=150,height=50,width=200)
sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=170,height=5,width=30)
commonNameResult_labl=Label(root, text="Sunflower",bd=4, height=1, width=12, font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0",relief='sunken')
commonNameResult_labl.place(x=700,y=150,height=50,width=250)

scientificName_labl=Label(root, text="Scientific Name",bd=2, height=1, width=12, font=("Script MT Bold",18), fg="#FFFFF0",bg="#0aacf7",relief='groove')
scientificName_labl.place(x=450,y=215,height=50,width=200)
sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=234,height=5,width=30)
scientificResult_labl=Label(root, text="Helianthus",bd=4, height=1, width=12, font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0",relief='sunken')
scientificResult_labl.place(x=700,y=215,height=50,width=250)

familyName_labl=Label(root, text="Family Name",bd=2, height=1, width=12, font=("Script MT Bold",18), fg="#FFFFF0",bg="#0aacf7",relief='groove')
familyName_labl.place(x=450,y=280,height=50,width=200)
sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=299,height=5,width=30)
familyResult_labl=Label(root, text="Asteraceae",bd=4, height=1, width=12, font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0",relief='sunken')
familyResult_labl.place(x=700,y=280,height=50,width=250)

kingdomName_labl=Label(root, text="Kingdom Name",bd=2, height=1, width=12, font=("Script MT Bold",18), fg="#FFFFF0",bg="#0aacf7",relief='groove')
kingdomName_labl.place(x=450,y=345,height=50,width=200)
sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=364,height=5,width=30)
kingdomResult_labl=Label(root, text="Plantae",bd=4, height=1, width=12, font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0",relief='sunken')
kingdomResult_labl.place(x=700,y=345,height=50,width=250)

orderName_labl=Label(root, text="Order Name",bd=2, height=1, width=12, font=("Script MT Bold",18), fg="#FFFFF0",bg="#0aacf7",relief='groove')
orderName_labl.place(x=450,y=410,height=50,width=200)
sep_image=Label(fg="#FFFFF0",bg="#0aacf7").place(x=660,y=429,height=5,width=30)
orderResult_labl=Label(root, text="Asterales",bd=4, height=1, width=12, font=("Bookman Old Style",18), fg="#0aacf7",bg="#FFFFF0",relief='sunken')
orderResult_labl.place(x=700,y=410,height=50,width=250)

default_desc="""These flowers are unique in that they have the ability to provide energy in the form of nourishment 
and vibrancy—attributes which mirror the sun and the energy provided by its heat and light.
Sunflowers are known for being “happy” flowers, making them the perfect gift to bring joy to someone's (or your) day."""
description_lbl=Label(root, text="Description :",bd=2, height=1, width=12, font=("Script MT Bold",16), fg="#FFFFF0",bg="#0aacf7",relief='groove')
description_lbl.place(x=5,y=510,width=130)
description_txt=Text(root,wrap=WORD, bd=4, bg="#FFFFF0", fg='#0aacf7', height="5", width="50", font=("Bookman Old Style",14), padx=10,pady=5,relief='sunken')
description_txt.insert(INSERT,default_desc)
description_txt.config(state=DISABLED)
description_txt.place(x=10,y=540,height=100,width=900)


default_mean="""Sunflowers symbolize adoration, loyalty and longevity. Much of the meaning of sunflowers stems from its namesake, 
the sun itself. Sunflowers are known for being “happy” flowers, making them the perfect gift to bring joy to someone's (or your) day."""
meaning_lbl=Label(root, text="Interesting Fact :",bd=2, height=1, width=12, font=("Script MT Bold",16), fg="#FFFFF0",bg="#0aacf7",relief='groove')
meaning_lbl.place(x=5,y=655,width=180)
meaning_txt=Text(root, bd=4,wrap=WORD,bg="#FFFFF0", fg='#0aacf7', height="5", width="50", font=("Lucida Calligraphy",14), padx=10,pady=5,relief='sunken')
meaning_txt.insert(INSERT,default_mean)
meaning_txt.config(state=DISABLED)
meaning_txt.place(x=10,y=685,height=100,width=900)

root.iconbitmap("flower_1.ico")
root.mainloop()

