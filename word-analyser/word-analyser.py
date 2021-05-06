from tkinter import *
from operator import itemgetter
import requests
import json

list_words = []


def preprocess_input(line, window):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Accept-Charset': 'UTF-8'
    }

    params = (
        ('targetType', 'pos-token'),
        ('targetType', 'spelling-correction-token'),
        ('targetType', 'syntax-relation'),
        ('apikey', 'b11e0cc09d4d7b3c4c56116688dd27beae454257'),
    )

    line = line.replace('\n', ' ')
    data = '[ { "text" : "' + str(line) + '" } ]'

    response = requests.post('http://api.ispras.ru/texterra/v1/nlp', headers=headers, params=params, data=data.encode('utf-8'))
    parsed_string = json.loads(response.text)
    position = parsed_string[0]['annotations']['pos-token']
    word = parsed_string[0]['annotations']['spelling-correction-token']
    syntax = parsed_string[0]['annotations']['syntax-relation']
    i = 0
    while i < len(word):
        name_word = word[i]['value'].lower()
        char = position[i]['value']['characters']
        if position[i]['value']['tag'] == 'PUNCT':
            i += 1
            continue
        syntax_word = syntax[i]['value']
        param = ''
        if syntax_word:
            if syntax_word['type']:
                param = syntax_word['type']
        tags = [position[i]['value']['tag']]
        for j in char:
            tags.append(j['tag'])
        if param:
            tags.append(param)
        list_words.append({'name': name_word, 'param': tags})
        i += 1
    quitWindow(window)


root = Tk()
root.title("DICTIONARY")
root.resizable(width=False, height=False)
root.geometry("500x350+200+200")


def inputWindow():
    children = Toplevel(root)
    children.title('Input word and sentence')
    children.geometry("500x350+200+200")
    calculated_text = Text(children, height=10, width=50)
    scrollbar = Scrollbar(children, command=calculated_text.yview)
    scrollbar.grid(row=4, column=4, sticky='nsew')
    calculated_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    calculated_text.configure(yscrollcommand=scrollbar.set)
    button = Button(children, width=25, text="Send", command=lambda: preprocess_input(calculated_text.get(1.0, END), children))
    button.grid(row=5, column=1, sticky=E, padx=5, pady=8, )


def quitWindow(window):
    window.destroy()


def helpWindow():
    children = Toplevel(root)
    children.title('Helper')
    children.geometry("500x350+200+200")
    calculated_text = Text(children, height=15, width=50)
    scrollbar = Scrollbar(children, command=calculated_text.yview)
    scrollbar.grid(row=4, column=4, sticky='nsew')
    calculated_text.grid(row=4, column=0, sticky='nsew', columnspan=3)
    calculated_text.configure(yscrollcommand=scrollbar.set)
    calculated_text.insert('end', 'A       прилагательное\nPR       предлог\nCONJ        союз\nS         существительное\nNUM       числительное')
    calculated_text.configure(state='disabled')


def viewWindow():
    list_words.sort(key=itemgetter('name'))
    children = Toplevel(root)
    children.title('View dictionary')
    children.geometry("500x350+200+200")
    list_box = Listbox(children, height=10, width=65)
    scrollbar = Scrollbar(children, command=list_box.yview)
    scrollbar.grid(row=4, column=4, sticky='nsew')
    list_box.grid(row=4, column=0, sticky='nsew', columnspan=3)
    list_box.configure(yscrollcommand=scrollbar.set)
    button = Button(children, width=25, text="Ok", command=lambda: quitWindow(children))
    button.grid(row=5, column=1, sticky=E, padx=5, pady=8, )
    button = Button(children, text="Help?", command=helpWindow)
    button.grid(row=1, column=1, sticky=W, padx=5, pady=8, )
    i = len(list_words)-1
    while i >= 0:
        list_box.insert(0, str(list_words[i]['name']) + ' ' + str(list_words[i]['param']))
        i -= 1


input_button = Button(text="Input", width=25, command=inputWindow)
input_button.grid(row=5, column=4, sticky=N, padx=5, pady=8, )
view_button = Button(text="View", width=25, command=viewWindow)
view_button.grid(row=4, column=4, sticky=S, padx=5, pady=8, )

root.mainloop()
