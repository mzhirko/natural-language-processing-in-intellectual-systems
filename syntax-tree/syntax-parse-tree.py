import nltk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
root = Tk()
root.title("Syntax parse tree")
root.resizable(width=False, height=False)
root.geometry("480x120+300+300")
label = Label(root, text='Input text:')
label.grid(row=1, column=0)
calculated_text = Text(root, height=5, width=40)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=3, rowspan=3)

grammar = r"""
        V: {<V.*>}
        N: {<NN.*|PRP>}
        P: {<IN>}
        NP: {<N|PP>+<DT|CD|PR.*|JJ|CC>}
        NP: {<DT|CD|PR.*|JJ|CC><N|PP>+}
        NP: {<DT><NP>}
        PP: {<P><NP>}
        VP: {<NP|N><V.*>}
        VP: {<V.*><NP|N>}
        VP: {<VP><PP>}
        """


def open_file_and_input_text():
    file_name = fd.askopenfilename(filetypes=(("Txt files", "*.txt"),))
    if file_name != '':
        with open(file_name, 'r') as file:
            text = file.read()
            text.replace('\n', '')
            calculated_text.delete(1.0, END)
            calculated_text.insert(1.0, text)


def information():
    messagebox.askquestion("Help", "1. Input text or open the .docx file.\n"
                                   "2. Clik on button 'Ok'.\n"
                                   "3. Look at the painted syntax tree.", type='ok')


def tokenize_text(doc):
    text_without_punct = []
    for item in doc:
        if item[1] != ',' and item[1] != '.':
            text_without_punct.append(item)
    return text_without_punct


def draw_syntax_tree():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc)
        text_without_punct = tokenize_text(doc)
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(text_without_punct)
        result.draw()


button1 = Button(text="Ok", width=10, command=draw_syntax_tree)
button1.grid(row=1, column=4)
button2 = Button(text="Open file", width=10, command=open_file_and_input_text)
button2.grid(row=2, column=4)
button3 = Button(text="Help?", width=10, command=information)
button3.grid(row=3, column=4)
root.mainloop()
