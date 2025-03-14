import re
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
import random

# ===============================
# Análisis Léxico
# ===============================
class Lexer:
    def __init__(self, rules):
        self.rules = [(re.compile(pattern), token_type) for pattern, token_type in rules]

    def tokenize(self, text):
        tokens = []
        position = 0
        while position < len(text):
            match = None
            for pattern, token_type in self.rules:
                match = pattern.match(text, position)
                if match:
                    if token_type:
                        tokens.append((token_type, match.group(0)))
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Illegal character at position {position}: '{text[position]}'")
        return tokens

# ===============================
# Análisis Sintáctico
# ===============================
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def consume(self, expected_type):
        current = self.peek()
        if current and current[0] == expected_type:
            self.position += 1
            return current
        raise SyntaxError(f"Expected {expected_type}, found {current}")

    def parse_program(self):
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        return ('program', statements)

    def parse_statement(self):
        if self.peek()[0] == 'PRINT':
            return self.parse_print_statement()
        elif self.peek()[0] == 'VAR':
            return self.parse_assignment()
        elif self.peek()[0] == 'MOVER_ARRIBA':
            return self.parse_move_up()
        elif self.peek()[0] == 'MOVER_ABAJO':
            return self.parse_move_down()
        elif self.peek()[0] == 'MOVER_IZQUIERDA':
            return self.parse_move_left()
        elif self.peek()[0] == 'MOVER_DERECHA':
            return self.parse_move_right()
        elif self.peek()[0] == 'INICIAR_JUEGO':
            return self.parse_start_game()
        elif self.peek()[0] == 'DETENER_JUEGO':
            return self.parse_stop_game()
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def parse_print_statement(self):
        self.consume('PRINT')
        expression = self.parse_expression()
        return ('print', expression)

    def parse_assignment(self):
        var_name = self.consume('VAR')[1]
        self.consume('EQUALS')
        value = self.parse_expression()
        return ('assign', var_name, value)

    def parse_expression(self):
        term = self.parse_term()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS', 'MOD', 'POW'):
            operator = self.consume(self.peek()[0])
            next_term = self.parse_term()
            term = ('binary_op', operator[1], term, next_term)
        return term

    def parse_term(self):
        factor = self.parse_factor()
        while self.peek() and self.peek()[0] in ('MULT', 'DIV'):
            operator = self.consume(self.peek()[0])
            next_factor = self.parse_factor()
            factor = ('binary_op', operator[1], factor, next_factor)
        return factor

    def parse_factor(self):
        if self.peek()[0] == 'LPAREN':
            self.consume('LPAREN')
            expression = self.parse_expression()
            self.consume('RPAREN')
            return expression
        elif self.peek()[0] == 'NUMBER':
            return ('number', self.consume('NUMBER')[1])
        elif self.peek()[0] == 'STRING':
            return ('string', self.consume('STRING')[1])
        elif self.peek()[0] == 'VAR':
            return ('var', self.consume('VAR')[1])
        else:
            raise SyntaxError(f"Unexpected token: {self.peek()}")

    def parse_move_up(self):
        self.consume('MOVER_ARRIBA')
        return ('move_up',)

    def parse_move_down(self):
        self.consume('MOVER_ABAJO')
        return ('move_down',)

    def parse_move_left(self):
        self.consume('MOVER_IZQUIERDA')
        return ('move_left',)

    def parse_move_right(self):
        self.consume('MOVER_DERECHA')
        return ('move_right',)

    def parse_start_game(self):
        self.consume('INICIAR_JUEGO')
        return ('start_game',)

    def parse_stop_game(self):
        self.consume('DETENER_JUEGO')
        return ('stop_game',)

# ===============================
# Ejecución del Árbol Sintáctico INTERPRETER
# ===============================
class Interpreter:
    def __init__(self):
        self.variables = {}
        self.game = None

    def evaluate(self, node):
        if node[0] == 'program':
            for statement in node[1]:
                self.evaluate(statement)
        elif node[0] == 'print':
            value = self.evaluate(node[1])
            output_text.insert(tk.END, f"{value}\n")
        elif node[0] == 'assign':
            var_name = node[1]
            value = self.evaluate(node[2])
            self.variables[var_name] = value
        elif node[0] == 'binary_op':
            left = self.evaluate(node[2])
            right = self.evaluate(node[3])
            operator = node[1]
            if operator == '+':
                return self._handle_addition(left, right)
            elif operator == '-':
                return self._handle_subtraction(left, right)
            elif operator == '*':
                return self._handle_multiplication(left, right)
            elif operator == '/':
                return self._handle_division(left, right)
            elif operator == '%':
                return self._handle_modulo(left, right)
            elif operator == '^':
                return self._handle_power(left, right)
        elif node[0] == 'var':
            var_name = node[1]
            if var_name in self.variables:
                return self.variables[var_name]
            raise NameError(f"Variable '{var_name}' not defined")
        elif node[0] == 'number':
            return float(node[1]) if '.' in node[1] else int(node[1])
        elif node[0] == 'string':
            return node[1][1:-1]  # Eliminar comillas
        elif node[0] == 'move_up':
            if self.game:
                self.game.change_direction('Up')
        elif node[0] == 'move_down':
            if self.game:
                self.game.change_direction('Down')
        elif node[0] == 'move_left':
            if self.game:
                self.game.change_direction('Left')
        elif node[0] == 'move_right':
            if self.game:
                self.game.change_direction('Right')
        elif node[0] == 'start_game':
            if not self.game:
                game_window = tk.Toplevel(root)
                self.game = SnakeGame(game_window)
        elif node[0] == 'stop_game':
            if self.game:
                self.game.master.destroy()
                self.game = None
        else:
            raise RuntimeError(f"Unknown node type: {node[0]}")

    def _handle_addition(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right
        elif isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)  # Conversión automática a string
        else:
            raise TypeError(f"Unsupported types for +: {type(left)} and {type(right)}")

    def _handle_multiplication(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left * right
        elif (isinstance(left, str) and isinstance(right, int)) or (isinstance(right, str) and isinstance(left, int)):
            return left * right if isinstance(left, int) else right * left
        else:
            raise TypeError(f"Unsupported types for *: {type(left)} and {type(right)}")

    def _handle_subtraction(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left - right
        raise TypeError(f"Unsupported types for -: {type(left)} and {type(right)}")

    def _handle_division(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left / right
        raise TypeError(f"Unsupported types for /: {type(left)} and {type(right)}")

    def _handle_modulo(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left % right
        raise TypeError(f"Unsupported types for %: {type(left)} and {type(right)}")

    def _handle_power(self, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left ** right
        raise TypeError(f"Unsupported types for ^: {type(left)} and {type(right)}")

# ===============================
# Juego de la Serpiente
# ===============================
class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Juego de la Serpiente")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0

        self.master.bind("<KeyPress>", self.change_direction)
        self.update()

    def create_food(self):
        x = random.randint(0, 19) * 20
        y = random.randint(0, 19) * 20
        self.food = (x, y)
        return self.food

    def change_direction(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            if (key == "Up" and self.direction != "Down") or \
               (key == "Down" and self.direction != "Up") or \
               (key == "Left" and self.direction != "Right") or \
               (key == "Right" and self.direction != "Left"):
                self.direction = key

    def update(self):
        head = self.snake[0]
        if self.direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 20)
        elif self.direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + 20, head[1])

        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= 400 or new_head[1] < 0 or new_head[1] >= 400:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.create_food()
        else:
            self.snake.pop()

        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="red")
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white")

        self.master.after(100, self.update)

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Arial", 24))
        self.canvas.create_text(200, 230, text=f"Final Score: {self.score}", fill="white", font=("Arial", 16))

# ===============================
# Interfaz Gráfica
# ===============================
def run_program():
    program = input_text.get("1.0", tk.END).strip()
    output_text.delete("1.0", tk.END)

    try:
        tokens = lexer.tokenize(program)
        parser = Parser(tokens)
        syntax_tree = parser.parse_program()
        interpreter = Interpreter()
        interpreter.evaluate(syntax_tree)
    except SyntaxError as e:
        output_text.insert(tk.END, f"Error de sintaxis: {e}\n")
    except NameError as e:
        output_text.insert(tk.END, f"Error de nombre: {e}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error durante la ejecución: {e}\n")

def clear_output():
    output_text.delete("1.0", tk.END)

def save_code():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(input_text.get("1.0", tk.END))

def load_code():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

def show_lexical_syntax_analysis():
    program = input_text.get("1.0", tk.END).strip()
    if not program:
        messagebox.showwarning("Advertencia", "No hay código para analizar.")
        return

    try:
        tokens = lexer.tokenize(program)
        lexical_text.delete("1.0", tk.END)
        lexical_text.insert(tk.END, f"Tokens: {tokens}\n")

        parser = Parser(tokens)
        syntax_tree = parser.parse_program()
        syntax_text.delete("1.0", tk.END)
        syntax_text.insert(tk.END, f"Árbol Sintáctico: {syntax_tree}\n")
    except SyntaxError as e:
        messagebox.showerror("Error de sintaxis", f"Error de sintaxis: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el análisis: {e}")

def toggle_theme():
    global current_theme
    if current_theme == "dark":
        current_theme = "light"
        root.configure(bg="#f0f0f0")
        style.configure("TLabelFrame", background="#f0f0f0", foreground="black")
        style.configure("TButton", background="#e0e0e0", foreground="black", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#d0d0d0")])
        input_text.config(bg="#ffffff", fg="black", insertbackground="black")
        output_text.config(bg="#ffffff", fg="black", insertbackground="black")
        lexical_text.config(bg="#ffffff", fg="black", insertbackground="black")
        syntax_text.config(bg="#ffffff", fg="black", insertbackground="black")
    else:
        current_theme = "dark"
        root.configure(bg="#1e1e1e")
        style.configure("TLabelFrame", background="#2e2e2e", foreground="white")
        style.configure("TButton", background="#3e3e3e", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#5e5e5e")])
        input_text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        output_text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        lexical_text.config(bg="#1e1e1e", fg="white", insertbackground="white")
        syntax_text.config(bg="#1e1e1e", fg="white", insertbackground="white")

# Crear ventana principal
root = tk.Tk()
root.title("Mini Python Interpreter - Visual Studio Style")
root.geometry("1200x800")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

# Estilo TTK
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabelFrame", background="#2e2e2e", foreground="white")
style.configure("TButton", background="#3e3e3e", foreground="white", font=("Segoe UI", 10, "bold"))
style.map("TButton", background=[("active", "#5e5e5e")])

# Menú
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=load_code)
file_menu.add_command(label="Guardar", command=save_code)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Limpiar Consola", command=clear_output)
menu_bar.add_cascade(label="Editar", menu=edit_menu)

view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Cambiar Tema", command=toggle_theme)
menu_bar.add_cascade(label="Ver", menu=view_menu)

root.config(menu=menu_bar)

# Panel de código (izquierda)
frame_input = ttk.LabelFrame(root, text="Código")
frame_input.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

input_text = scrolledtext.ScrolledText(frame_input, width=80, height=30, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12))
input_text.pack(padx=5, pady=5, fill="both", expand=True)

# Panel de análisis léxico/sintáctico (derecha)
frame_analysis = ttk.LabelFrame(root, text="Análisis Léxico y Sintáctico")
frame_analysis.pack(side=tk.RIGHT, padx=10, pady=10, fill="both", expand=True)

lexical_text = scrolledtext.ScrolledText(frame_analysis, width=40, height=15, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12))
lexical_text.pack(padx=5, pady=5, fill="both", expand=True)

syntax_text = scrolledtext.ScrolledText(frame_analysis, width=40, height=15, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12))
syntax_text.pack(padx=5, pady=5, fill="both", expand=True)

# Panel de salida (abajo)
frame_output = ttk.LabelFrame(root, text="Salida")
frame_output.pack(side=tk.BOTTOM, padx=10, pady=10, fill="both", expand=True)

output_text = scrolledtext.ScrolledText(frame_output, width=120, height=10, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 12))
output_text.pack(padx=5, pady=5, fill="both", expand=True)

# Botones
frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.TOP, pady=5)

run_button = ttk.Button(frame_buttons, text="Ejecutar", command=run_program)
run_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(frame_buttons, text="Limpiar", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=5)

analysis_button = ttk.Button(frame_buttons, text="Análisis Léxico/Sintáctico", command=show_lexical_syntax_analysis)
analysis_button.pack(side=tk.LEFT, padx=5)

# Reglas léxicas
rules = [
    (r'print', 'PRINT'),
    (r'MOVER_ARRIBA', 'MOVER_ARRIBA'),
    (r'MOVER_ABAJO', 'MOVER_ABAJO'),
    (r'MOVER_IZQUIERDA', 'MOVER_IZQUIERDA'),
    (r'MOVER_DERECHA', 'MOVER_DERECHA'),
    (r'INICIAR_JUEGO', 'INICIAR_JUEGO'),
    (r'DETENER_JUEGO', 'DETENER_JUEGO'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'VAR'),
    (r'\d+\.?\d*', 'NUMBER'),
    (r'=', 'EQUALS'),
    (r'\+', 'PLUS'),
    (r'\-', 'MINUS'),
    (r'\*', 'MULT'),
    (r'/', 'DIV'),
    (r'%', 'MOD'),
    (r'\^', 'POW'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\s+', None),
    (r'\"[^\"]*\"', 'STRING'),
    (r"\'[^\']*\'", 'STRING'),
]

lexer = Lexer(rules)
current_theme = "dark"
root.mainloop()
