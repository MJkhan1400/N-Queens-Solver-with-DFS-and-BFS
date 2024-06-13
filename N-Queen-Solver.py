import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from queue import Queue
import time

class NQueens:
    def __init__(self, size):
        self.size = size

    def solve_dfs(self):
        if self.size < 1:
            return []
        solutions = []
        stack = [[]]
        start_time = time.time()
        while stack:
            solution = stack.pop()
            if self.conflict(solution):
                continue
            row = len(solution)
            if row == self.size:
                solutions.append(solution)
                continue
            for col in range(self.size):
                queen = (row, col)
                queens = solution.copy()
                queens.append(queen)
                stack.append(queens)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return solutions, elapsed_time

    def solve_bfs(self):
        if self.size < 1:
            return []
        solutions = []
        queue = Queue()
        queue.put([])
        start_time = time.time()
        while not queue.empty():
            solution = queue.get()
            if self.conflict(solution):
                continue
            row = len(solution)
            if row == self.size:
                solutions.append(solution)
                continue
            for col in range(self.size):
                queen = (row, col)
                queens = solution.copy()
                queens.append(queen)
                queue.put(queens)
        end_time = time.time()
        elapsed_time = end_time - start_time
        return solutions, elapsed_time

    def conflict(self, queens):
        for i in range(1, len(queens)):
            for j in range(0, i):
                a, b = queens[i]
                c, d = queens[j]
                if a == c or b == d or abs(a - c) == abs(b - d):
                    return True
        return False


def main():
    def start_solver():
        try:
            board_size = int(size_entry.get())
            if board_size < 1:
                messagebox.showerror("Error", "Please enter a positive integer.")
                return
            dfs_solver = NQueens(board_size)
            bfs_solver = NQueens(board_size)

            global dfs_solutions, bfs_solutions, dfs_time_taken, bfs_time_taken
            dfs_solutions, dfs_time_taken = dfs_solver.solve_dfs()
            bfs_solutions, bfs_time_taken = bfs_solver.solve_bfs()

            dfs_board_solution.config(text=f"One of the Solutions: ")
            dfs_solution_count_label.config(text=f"Number of solutions (DFS): {len(dfs_solutions)}")
            dfs_time_label.config(text=f"Time taken (DFS): {dfs_time_taken:.6f} seconds")
            display_solution(dfs_board_canvas, dfs_solutions)

            bfs_board_solution.config(text=f"One of the Solutions: ")
            bfs_solution_count_label.config(text=f"Number of solutions (BFS): {len(bfs_solutions)}")
            bfs_time_label.config(text=f"Time Taken (BFS): {bfs_time_taken:.6f} seconds")
            display_solution(bfs_board_canvas, bfs_solutions)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")


    queen_photos = []

    def display_solution(canvas, solutions):
        canvas.delete("all")
        square_size = 400 // len(solutions[0])
        
        # Load the PNG image of a queen
        queen_image = Image.open("queen.png")
        queen_image = queen_image.resize((square_size, square_size), Image.LANCZOS)
        queen_photo = ImageTk.PhotoImage(queen_image)
        queen_photos.append(queen_photo)

        for row in range(len(solutions[0])):
            for col in range(len(solutions[0])):
                color = "wheat" if (row + col) % 2 == 0 else "#00001A"
                canvas.create_rectangle(col * square_size, row * square_size, (col + 1) * square_size, (row + 1) * square_size, fill=color)
                if (row, col) in solutions[0]:
                    canvas.create_image(col * square_size + square_size // 2, row * square_size + square_size // 2, image=queen_photo)


    root = tk.Tk()
    root.title("N-Queens Solver")
    root.geometry("1080x1080")
    root.configure(bg="#00001A")

    title_label = tk.Label(root, text="N-Queens Solver", font=("Arial", 34), bg="#00001A", fg="wheat")
    title_label.pack(pady=(60, 5))  # Adding vertical padding

    description_label = tk.Label(root, text="By Mohammad Jazib Khan", font=("Arial", 14), bg="#00001A", fg="wheat", wraplength=800)
    description_label.pack(pady=(0, 20))  # Adding vertical padding
    
    description_label2 = tk.Label(root, text="This program solves the N-Queens problem using Depth-First Search (DFS) and Breadth-First Search (BFS) algorithms and displays the output as a comparision between the algorithms.\n The recommended board sizes to enter are 4 and 8", font=("Arial", 12), bg="#00001A", fg="wheat", wraplength=800)
    description_label2.pack(pady=(10, 10))  # Adding vertical padding

    input_frame = tk.Frame(root, bg="#00001A")
    input_frame.pack(pady=20)

    size_label = tk.Label(input_frame, text="Enter board size:", font=("Arial", 16), bg="#00001A", fg="wheat")
    size_label.grid(row=0, column=0, padx=(10, 5), pady=10)

    size_entry = tk.Entry(input_frame, font=("Arial", 16), bd=2, relief=tk.SUNKEN, borderwidth=4, border=4, bg="wheat")  # Styled input box with white background
    size_entry.grid(row=0, column=1, padx=(5, 10), pady=10, ipady=3)  # Setting internal padding for height

    start_button = tk.Button(input_frame, text="Start", font=("Arial", 14, "bold"), command=start_solver, bg="#00001A", fg="wheat", relief=tk.RAISED, width=10, bd=4, activebackground="wheat")  # Styled button
    start_button.grid(row=0, column=2, pady=10, padx=(0, 10))  # Setting internal padding for width

    # Hover effect on button
    start_button.bind("<Enter>", lambda event: start_button.config(bg="wheat", fg="#00001A"))
    start_button.bind("<Leave>", lambda event: start_button.config(bg="#00001A", fg="wheat"))

    comparison_frame = tk.Frame(root, bg="#00001A")
    comparison_frame.pack()

    dfs_frame = tk.Frame(comparison_frame, bg="#00001A")
    dfs_frame.pack(side=tk.LEFT, padx=(20, 10), pady=10)


    dfs_board_label = tk.Label(dfs_frame, text="Deapth First Search Algorithm Solution", font=("Arial", 16), bg="#00001A", fg="wheat")
    dfs_board_label.pack(pady=5)
    
    dfs_board_solution = tk.Label(dfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    dfs_board_solution.pack(pady=5)
    
    dfs_board_canvas = tk.Canvas(dfs_frame, width=400, height=400, bd=2, relief=tk.SUNKEN, bg="wheat")
    dfs_board_canvas.pack(pady=(5, 20))
    
    dfs_solution_count_label = tk.Label(dfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    dfs_solution_count_label.pack(pady=(10, 5))

    dfs_time_label = tk.Label(dfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    dfs_time_label.pack(pady=5)

    bfs_frame = tk.Frame(comparison_frame, bg="#00001A")
    bfs_frame.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

    bfs_board_label = tk.Label(bfs_frame, text="Breadth First Search Algorithm Solution", font=("Arial", 16), bg="#00001A", fg="wheat")
    bfs_board_label.pack(pady=5)
    
    bfs_board_solution = tk.Label(bfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    bfs_board_solution.pack(pady=5)

    bfs_board_canvas = tk.Canvas(bfs_frame, width=400, height=400, bd=2, relief=tk.SUNKEN, bg="wheat")
    bfs_board_canvas.pack(pady=(5, 20))

    bfs_solution_count_label = tk.Label(bfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    bfs_solution_count_label.pack(pady=(10, 5))

    bfs_time_label = tk.Label(bfs_frame, text="", font=("Arial", 16), bg="#00001A", fg="wheat")
    bfs_time_label.pack(pady=5)

    root.mainloop()


if __name__ == '__main__':
    main()
