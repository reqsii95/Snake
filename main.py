import tkinter as tk
import random
import winsound
import math

class SnakeNoirUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake by reqsi")
        self.root.configure(bg="#000")
        self.root.resizable(False, False)
        
        self.width, self.height = 600, 400
        self.cell = 20
        
        # Google Pixel / Retro UI Fontları
        self.font_bg = ("ByteBounce", 140, "bold")
        self.font_title = ("ByteBounce", 45, "bold")
        self.font_pixel = ("ByteBounce", 12, "bold")
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="#000", 
                               highlightthickness=1, highlightbackground="#222", bd=0)
        self.canvas.pack(pady=40, padx=40)

        self.root.bind("<KeyPress>", self.control)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_hover)
        
        self.state = "MENU"
        self.score = 0
        self.high_score = 0
        self.hover_alpha = 0 
        self.target_alpha = 0
        self.food_pulse = 0
        self.shake_time = 0
        
        self.update()

    def play_sound(self, s_type):
        try:
            if s_type == "eat": winsound.Beep(1800, 20)
            elif s_type == "death": winsound.Beep(200, 300)
        except: pass

    def reset(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.dir = "Right"
        self.score = 0
        self.spawn_food()

    def spawn_food(self):
        self.food = (random.randint(0, (self.width-self.cell)//self.cell)*self.cell,
                     random.randint(0, (self.height-self.cell)//self.cell)*self.cell)

    def control(self, e):
        if self.state == "PLAYING":
            opp = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
            if e.keysym in opp and e.keysym != opp.get(self.dir):
                self.dir = e.keysym

    def handle_hover(self, event):
        on_btn = 220 <= event.x <= 380 and (220 <= event.y <= 270 if self.state=="MENU" else 250 <= event.y <= 300)
        self.target_alpha = 1 if on_btn else 0

    def animate_logic(self):
        if self.hover_alpha < self.target_alpha: self.hover_alpha = min(1, self.hover_alpha + 0.15)
        elif self.hover_alpha > self.target_alpha: self.hover_alpha = max(0, self.hover_alpha - 0.15)
        self.food_pulse = (self.food_pulse + 0.15) % (2 * math.pi)
        if self.shake_time > 0: self.shake_time -= 1

    def handle_click(self, event):
        if self.target_alpha == 1:
            self.state = "PLAYING"
            self.reset()

    def update(self):
        self.animate_logic()
        if self.state == "PLAYING":
            hx, hy = self.snake[0]
            if self.dir == "Up": hy -= self.cell
            elif self.dir == "Down": hy += self.cell
            elif self.dir == "Left": hx -= self.cell
            elif self.dir == "Right": hx += self.cell
            
            new_head = (hx, hy)
            if hx < 0 or hx >= self.width or hy < 0 or hy >= self.height or new_head in self.snake:
                self.play_sound("death")
                self.state = "GAMEOVER"
                if self.score > self.high_score: self.high_score = self.score
            else:
                self.snake.insert(0, new_head)
                if new_head == self.food:
                    self.play_sound("eat")
                    self.score += 1
                    self.shake_time = 4
                    self.spawn_food()
                else: self.snake.pop()
        
        self.draw()
        self.root.after(70, self.update)

    def draw_button(self, x, y, text):
        w, h = 160, 48
        v = int(255 * self.hover_alpha)
        color = f'#{v:02x}{v:02x}{v:02x}'
        text_color = "black" if self.hover_alpha > 0.5 else "white"
        
        # Temiz Buton Çizimi (Sıfır Çizgi Hatası)
        self.canvas.create_oval(x-w/2, y-h/2, x-w/2+h, y+h/2, fill=color, outline="")
        self.canvas.create_oval(x+w/2-h, y-h/2, x+w/2, y+h/2, fill=color, outline="")
        self.canvas.create_rectangle(x-w/2+h/2, y-h/2, x+w/2-h/2, y+h/2, fill=color, outline="")
        
        # Pasif durumdayken çok ince dış çerçeve
        if self.hover_alpha < 0.1:
            self.canvas.create_arc(x-w/2, y-h/2, x-w/2+h, y+h/2, start=90, extent=180, outline="#444", style="arc")
            self.canvas.create_arc(x+w/2-h, y-h/2, x+w/2, y+h/2, start=270, extent=180, outline="#444", style="arc")
            self.canvas.create_line(x-w/2+h/2, y-h/2, x+w/2-h/2, y-h/2, fill="#444")
            self.canvas.create_line(x-w/2+h/2, y+h/2, x+w/2-h/2, y+h/2, fill="#444")

        self.canvas.create_text(x, y, text=text, fill=text_color, font=self.font_pixel)

    def draw(self):
        self.canvas.delete("all")
        
        if self.shake_time > 0:
            dx, dy = random.randint(-2, 2), random.randint(-2, 2)
            self.canvas.move("all", dx, dy)
            
        if self.state == "MENU":
            self.canvas.create_text(300, 150, text="Snake", fill="white", font=self.font_title)
            self.draw_button(300, 245, "Start Game")
            
        elif self.state == "PLAYING":
            # Arka Plan Dev Skor
            self.canvas.create_text(300, 200, text=f"{self.score}", fill="#080808", font=self.font_bg)
            
            # ELMA ANİMASYONU: Sadece Renk Değişimi (Nefes Alma Efekti)
            c_val = int(140 + 115 * (0.5 + 0.5 * math.sin(self.food_pulse)))
            f_color = f'#{c_val:02x}{c_val:02x}{c_val:02x}'
            self.canvas.create_oval(self.food[0]+6, self.food[1]+6, self.food[0]+14, self.food[1]+14, fill=f_color, outline="")
            
            # Yılan
            for i, (x, y) in enumerate(self.snake):
                c = "white" if i == 0 else f"#{max(25, 160-i*10):02x}{max(25, 160-i*10):02x}{max(25, 160-i*10):02x}"
                self.canvas.create_oval(x+2, y+2, x+18, y+18, fill=c, outline="")
                
        elif self.state == "GAMEOVER":
            self.canvas.create_text(300, 130, text="Game Over", fill="white", font=self.font_title)
            self.canvas.create_text(300, 195, text=f"Score:{self.score} | Best:{self.high_score}", fill="#444", font=self.font_pixel)
            self.draw_button(300, 275, "Try Again")

if __name__ == "__main__":
    app = tk.Tk()
    SnakeNoirUltimate(app)
    app.mainloop()