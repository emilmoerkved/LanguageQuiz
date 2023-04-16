import tkinter as tk
from tkinter import ttk, NW, filedialog
from PIL import ImageTk, Image

from game import Quiz


LARGE_FONT = ('Verdana', 24)


class GraphicalUserInterface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Language Quiz")
        self.height = 480
        self.width = 680
        self.geometry("{}x{}".format(self.width, self.height))
        self.resizable(False, False)
        self.grid_rows = 15
        self.grid_columns = 2

        self.container = tk.Frame(self)
        for i in range(self.grid_rows):
            self.grid_rowconfigure(i, weight=1)
        for i in range(self.grid_columns):
            self.grid_columnconfigure(i, weight=1)

        self.container.grid(row=0, column=0, rowspan=self.grid_rows, columnspan=self.grid_columns, sticky='nsew')
        for i in range(self.grid_rows):
            self.container.grid_rowconfigure(i, weight=1)
        for i in range(self.grid_columns):
            self.container.grid_columnconfigure(i, weight=1)

        self.file = ''
        self.quiz = ''

        self.frames = {}
        for F in (StartPage, Question, EndOfGame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, rowspan=self.grid_rows, columnspan=self.grid_columns, sticky='nsew')
        self.show_frame(StartPage)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()

    def start_game(self):
        self.file = filedialog.askopenfilename(initialdir=r'C:\Users\Emil\PycharmProjects\LanguageQuiz\Dictionaries')
        if self.file:
            self.quiz = Quiz(self.file)
            self.show_frame(Question)
            self.frames[Question].next_question(self)
        else:
            self.show_frame(StartPage)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):  # parent = container, controller = GraphicalUserInterface
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('my.TButton', font=('Helvetica', 46), foreground='blue')

        for i in range(controller.grid_rows):
            self.rowconfigure(i, weight=1)
        for i in range(controller.grid_columns):
            self.columnconfigure(i, weight=1)

        file_bg = Image.open('Backgrounds/background_gradient_blue.png')
        img_bg = ImageTk.PhotoImage(file_bg)
        c_bg = tk.Canvas(self, width=controller.width, height=controller.height)
        c_bg.place(x=0, y=0)
        self.img_bg = img_bg
        c_bg.create_image(0, 0, anchor=NW, image=img_bg)

        title_label = ttk.Label(self, text="Language Quiz", font=('Verdana', 24), background='#C9CCD6')
        title_label.grid(column=0, row=0, columnspan=controller.grid_columns)

        start_game_button = ttk.Button(self, text="Start game", style='my.TButton',
                                       command=lambda c=controller: controller.start_game())
        start_game_button.grid(column=0, row=10, columnspan=controller.grid_columns, sticky='nsew')


class Question(tk.Frame):

    def __init__(self, parent, controller):  # parent = container, controller = GraphicalUserInterface
        tk.Frame.__init__(self, parent)

        for i in range(controller.grid_rows):
            self.rowconfigure(i, weight=1)
        for i in range(controller.grid_columns):
            self.columnconfigure(i, weight=1)

        file_bg = Image.open('Backgrounds/background_gradient_blue.png')
        img_bg = ImageTk.PhotoImage(file_bg)
        c_bg = tk.Canvas(self, width=controller.width, height=controller.height)
        c_bg.place(x=0, y=0)
        self.img_bg = img_bg
        c_bg.create_image(0, 0, anchor=tk.NW, image=img_bg)

        self.delay = 1000  # milliseconds, waiting time used for response in quiz
        self.wait_var = tk.BooleanVar()
        self.wait_var.set(False)

    def next_question(self, controller):
        controller.quiz.next_question()

        style = ttk.Style()
        style.theme_use('clam')  # clam is used to be able to modify background color.
        style.configure('Alt1.TButton', font=('Helvetica', 24), foreground='orange')
        style.configure('Alt2.TButton', font=('Helvetica', 24), foreground='blue')
        style.configure('Alt3.TButton', font=('Helvetica', 24), foreground='purple')

        def adjust_string(string):
            if len(string) > 21:
                text_split = string.split()
                string = ''
                line_length = 0
                for word in text_split:
                    if line_length > 18:
                        string += ' \n'  # new line
                        line_length = 0
                    elif string != '':
                        string += ' '  # white space if not first word
                        line_length += 1
                    string += word
                    line_length += len(word)
            return string

        self.question = ttk.Label(self, text=adjust_string(str(controller.quiz.question)),
                                  font=('Verdana', 24), background='#7CABEA')
        self.question.grid(column=0, row=6, rowspan=3)

        self.alt1 = ttk.Button(self, text=adjust_string(str(controller.quiz.alternatives[0])),
                              command=lambda: self._check_answer(controller.quiz.alternatives[0], controller),
                               style='Alt1.TButton')
        self.alt2 = ttk.Button(self, text=adjust_string(str(controller.quiz.alternatives[1])),
                              command=lambda: self._check_answer(controller.quiz.alternatives[1], controller),
                               style='Alt2.TButton')
        self.alt3 = ttk.Button(self, text=adjust_string(str(controller.quiz.alternatives[2])),
                              command=lambda: self._check_answer(controller.quiz.alternatives[2], controller),
                               style='Alt3.TButton')

        self.numb_questions_left = ttk.Label(self, text='{} questions left'.format(controller.quiz.questions_left),
                                             background='#3E77D2')

        self.alt1.grid(column=1, row=3, rowspan=3)
        self.alt2.grid(column=1, row=6, rowspan=3)
        self.alt3.grid(column=1, row=9, rowspan=3)
        self.numb_questions_left.grid(column=0, row=12)

    def _show_result_of_answer(self, alternative, result):
        style = ttk.Style()

        style.configure('Green.TButton', font=('Helvetica', 24), background='green')
        style.configure('Red.TButton', font=('Helvetica', 24), background='red')
        style.configure('Answered.TButton', font=('Helvetica', 24), background='gray71', foreground='black')
        style.map('Green.TButton', background=[('active', 'green')])
        style.map('Red.TButton', background=[('active', 'red')])

        if result == 'correct':
            background_style = 'Green.TButton'
        elif result == 'false':
            background_style = 'Red.TButton'

        def change_back_to_standard(button):
            button['style'] = 'Answered.TButton'
            self.wait_var.set(True)

        if alternative == self.alt1['text']:
            self.alt1['style'] = background_style
            self.alt1.after(self.delay, lambda: change_back_to_standard(self.alt1))
        elif alternative == self.alt2['text']:
            self.alt2['style'] = background_style
            self.alt2.after(self.delay, lambda: change_back_to_standard(self.alt2))
        elif alternative == self.alt3['text']:
            self.alt3['style'] = background_style
            self.alt3.after(self.delay, lambda: change_back_to_standard(self.alt3))

        self.wait_variable(self.wait_var)  # wait to show colors
        self.wait_var.set(False)

    def _clean_question(self, controller):
        self.question.destroy()
        self.alt1.destroy()
        self.alt2.destroy()
        self.alt3.destroy()
        self.numb_questions_left.destroy()
        if controller.quiz.more_questions():
            self.next_question(controller)
        else:
            style = ttk.Style()
            style.theme_use('vista')  # to go back to vista theme after quiz
            controller.show_frame(EndOfGame)

    def _check_answer(self, alternative, controller):
        if alternative == controller.quiz.answer:
            self._show_result_of_answer(alternative, 'correct')
            self._clean_question(controller)
        else:
            self._show_result_of_answer(alternative, 'false')


class EndOfGame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        style = ttk.Style()
        style.configure('my.TButton', font=('Helvetica', 46), foreground='blue')

        for i in range(controller.grid_rows):
            self.rowconfigure(i, weight=1)
        for i in range(controller.grid_columns):
            self.columnconfigure(i, weight=1)

        file_bg = Image.open('Backgrounds/background_gradient_blue.png')
        img_bg = ImageTk.PhotoImage(file_bg)
        c_bg = tk.Canvas(self, width=controller.width, height=controller.height)
        c_bg.place(x=0, y=0)
        self.img_bg = img_bg
        c_bg.create_image(0, 0, anchor=NW, image=img_bg)

        title_label = ttk.Label(self, text="Well Done!", font=('Verdana', 24), background='#C9CCD6')
        title_label.grid(column=0, row=0, columnspan=controller.grid_columns)

        start_game_button = ttk.Button(self, text="Return to start page", style='my.TButton',
                                       command=lambda c=controller: controller.show_frame(StartPage))
        start_game_button.grid(column=0, row=10, columnspan=controller.grid_columns, sticky='nsew')




