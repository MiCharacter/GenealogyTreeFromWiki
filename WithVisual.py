#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pyvis')
from bs4 import BeautifulSoup
import requests
import networkx as nx
from pyvis.network import Network
import json
from networkx.readwrite import json_graph
import tkinter
from tkinter.ttk import Combobox  

G = nx.Graph()
listifwas = []
listlinkifwas = []
nt = Network()
def f(url, state, name, koleno):
  if (koleno > 0):
    urladded = list(url)
    urladded.insert(0,"https://ru.wikipedia.org")
    urladded = "".join(urladded)
    try:
      page = requests.get(urladded)
      soup = BeautifulSoup(page.text, 'html.parser')
      everything = []
      relatives = []
      everything = soup.find_all('tr')
      for i in everything:
          if str(i).find('Отец') >0:
            relatives.append(i)
            
          if str(i).find('Мать') >0:
            relatives.append(i)
          
          if str(i).find('Супруг') >0:
            relatives.append(i)
          
          if str(i).find('Дети') >0:
            relatives.append(i)

      links = []
      relativesnames = []

      for i in relatives:
        a = list(i.text)

        b = 2
        while b!=len(a):
          if (a[b].isupper() and a[b-1] != ('-') and a[b-1] != (' ') and a[b]!= "I" and a[b]!= "V") or (a[b] =="и" and a[b-1]==" ") or a[b]==",":
            a.insert(b,"$")
            b = b + 1
          b = b + 1

        while True:
          try:
            a.remove('\n')
          except:
            break
        a = ''.join(a)
        a = a.split('$')
        relativesnames.append(a)

        position = str(i).find("/wiki/")
        if(position == -1):
          links.append("\nNone")
        b = 0
        while position > 0:
          if b == 0:
            links.append("\n")
          else:
            links.append("^^^")
          while list(str(i))[position] != '"' :
                      links.append(list(str(i))[position])
                      position = position + 1
          position = str(i).find("/wiki/",position)
          b = b + 1


      links = ''.join(links)
      links = links.split('\n')
      b = 1
      while b!= len(links):
        links[b] = links[b].split('^^^')
        b = b + 1
      try:
        links.remove("")
      except:
        0
      b = 1
      for i in links:
        if b == -1:
          break
        if b != state:
          c = 2
          for j in i:
            G.add_edge(name,relativesnames[b-1][c-1])
            if (relativesnames[b-1][c-1] in listifwas) or (links[b-1][c-2] in listlinkifwas) : 0
            else:
              listifwas.append(relativesnames[b-1][c-1])
              listlinkifwas.append(links[b-1][c-2])
              f(links[b-1][c-2], b, relativesnames[b-1][c-1], koleno-1)
            c = c + 1
        b = b + 1
    except: 0
    

file = open("data_file.json", "w")

window = tkinter.Tk()   
label1= tkinter.Label(window, text="Введите URL Страницы википедии"+'\n'+"того лица с которого хотите начать:")
label1.grid(column=0, row=0)

label1= tkinter.Label(window, text="До какого уровня \n просматривать родственников:")
label1.grid(column=0, row=1)

data = tkinter.StringVar()
data.set('Пример: \n /wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II')

label3= tkinter.Label(window, textvariable=data)
label3.grid(column=0, row=2)

entry_02 = tkinter.Entry(window, text='Пример: /wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II')
entry_02.grid(column=1, row=0)

combo = Combobox(window)  
combo['values'] = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
combo.current(0)
combo.grid(column=1, row=1)  

def click1():
    inf = entry_02.get()
    if inf != "":
        if inf[:6] == "/wiki/":
            data.set('Начинаю построение, ждите... \n Пример: \n /wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II')
            f(inf, 0, "Екатерина II", combo.current()+2)
            nt.from_nx(G)
            nt.show('net2.html')
        else:
            data.set('Это не ссылка на Вики! \n Пример: \n /wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II')
        None
    else:
        data.set('Введите данные! \n Пример: \n /wiki/%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B0_II')
    
def click2():
    data1 = json_graph.node_link_data(G)
    s1 = json.dumps(data1)
    file.write(s1)
    
button_01 = tkinter.Button(window, text = "Начать построение!", command = click1)
button_01.grid(column=1, row=3)

button_02 = tkinter.Button(window, text = "Сохранить результат", command = click2)
button_02.grid(column=1, row=4)



window.title("Построим дерево королевских особ за вас!")
window.mainloop()
file.close


# In[ ]:




