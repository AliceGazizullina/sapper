import tkinter as tk
import random
from random import shuffle
from tkinter.messagebox import showinfo
#добавила в гитхаб
colors = {
    0: 'gray',
    1: 'blue',
    2: 'green',
    3: '#a000b5',
    4: '#ff00ea',
    5: '#009eb0',
    6: '#92c700',
    7: '#0011c7',
    8: '#4600c7'
}


# Унаследованный клас от обычной кнопки
class MyButton(tk.Button):
    def __init__(self, master, x, y,number=0, *args, **kwargs):
        super(MyButton, self).__init__(master,width=3, font='Calibri 15 bold', *args, **kwargs )
        self.x = x 
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:
    window = tk.Tk()
    window.title('Саперский движ')
    Row = 10
    Columns = 10
    MINES = 10
    IS_GAME_OVER = False
    def __init__(self):
        # Создание сетки для игры сапер и кнопок
        self.buttons = []
        for i in range(MineSweeper.Row+2):
            temp = []
            for j in range(MineSweeper.Columns+2):
                btn = MyButton(MineSweeper.window,x=i,y=j)
                btn.config(command=lambda butt=btn: self.click(butt))
                temp.append(btn)
            self.buttons.append(temp)
    
    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text="*", background="red", disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли')
            for i in range(1,MineSweeper.Row+1):
                for j in range(1,MineSweeper.Columns+1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb,'black')
            
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)
    
    def breadth_first_search(self, btn: MyButton):

        queue = []
        while queue:
            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb,'black')

            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x,y = cur_btn.x, cur_btn.y
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        # if not abs(dx - dy) == 1:
                        #     continue

                        next_btn = self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<=next_btn.x<=MineSweeper.Row and \
                            1<=next_btn.y<=MineSweeper.Columns and next_btn not in queue:
                            queue.append(next_btn)



    def create_widgets(self):
        for i in range(1,MineSweeper.Row+1):
            for j in range(1,MineSweeper.Columns+1):
                btn = self.buttons[i][j]
                btn.grid(row=i,column=j)
        # Тут создание сетки заканчивается        
    
    def open_all_buttons(self):
        for i in range(MineSweeper.Row+2):
            for j in range(MineSweeper.Columns+2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background="red", disabledforeground='black')
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb,'black')
                    btn.config(text=btn.count_bomb, fg=color)
                

    
    #Вызов окна игры
    def start_game(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_buttons()
        self.print_button()
        # self.open_all_buttons()
        print(self.get_mines_places())

        MineSweeper.window.withdraw()
        second_window = tk.Toplevel(MineSweeper.window)
        second_window.title("Вопрос не на жизнь, а на смерть")
        second_window.geometry("500x300")
        second_window.configure(bg='pink')

        label2 = tk.Label(second_window, text="Ты лошарик?",font=("Courier", 20, "bold"), bg='pink')
        label2.pack(pady=20)

        label2 = tk.Label(second_window, text="(´• ω •`) ♡",font=("Courier", 20, "bold"), bg='pink')
        label2.pack(pady=30)

        def exit_program():
            MineSweeper.window.quit()  
            MineSweeper.window.destroy()  
    
        # Функция возврата в первое окно
        def return_to_first(window_to_close):
            window_to_close.destroy()
            showinfo('Супер', 'Я знала! Держи своего сапера')
            MineSweeper.window.deiconify()
        
        def move_window_randomly():
            screen_width = second_window.winfo_screenwidth()
            screen_height = second_window.winfo_screenheight()

            window_width = 500  
            window_height = 300

            x = random.randint(0, screen_width - window_width)
            y = random.randint(0, screen_height - window_height)

            second_window.geometry(f"+{x}+{y}")
        
        button_frame = tk.Frame(second_window, bg='pink')
        button_frame.pack(pady=20)
 
        return_button = tk.Button(button_frame, text="Да",font=("Courier", 20, "bold"), command=lambda: return_to_first(second_window))
        return_button.pack(side=tk.LEFT, padx=15)
    
        # Вторая кнопка "Нет" 
        move_button = tk.Button(button_frame, text="Нет",font=("Courier", 20, "bold"), command=move_window_randomly)
        move_button.pack(side=tk.LEFT, padx=15)

        second_window.protocol("WM_DELETE_WINDOW", exit_program)

        MineSweeper.window.mainloop()
    
    def print_button(self):
        for i in range(1,MineSweeper.Row+1):
            for j in range(1,MineSweeper.Columns+1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B',end='')
                else:
                    print(btn.count_bomb,end='')
            print()

    def insert_mines(self):
        index_mines = self.get_mines_places()
        print(index_mines)
        count = 1
        for i in range(1,MineSweeper.Row+1):
            for j in range(1,MineSweeper.Columns+1):
                btn = self.buttons[i][j]
                btn.number = count
                if btn.number in index_mines:
                    btn.is_mine = True
                count += 1
    
    def count_mines_in_buttons(self):
        for i in range(1,MineSweeper.Row+1):
            for j in range(1,MineSweeper.Columns+1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1,0,1]:
                        for col_dx in [-1,0,1]:
                            neighbour = self.buttons[i+row_dx ][j+col_dx]
                            if neighbour.is_mine:
                                count_bomb +=1
                btn.count_bomb = count_bomb
    # Создание мин 
    
    def get_mines_places(self):
        indexes = list(range(1,MineSweeper.Columns*MineSweeper.Row+1))
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper()



game.start_game()







