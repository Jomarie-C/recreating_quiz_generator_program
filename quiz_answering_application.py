import tkinter as tk
from tkinter import messagebox
import json
import random
import os

class QuizAnsweringApp:
    QUIZ_FILENAME = "quiz_generator.txt"

    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("🧠 Take a Quiz")
        self.root_window.geometry("500x400")
        self.root_window.resizable(False, False)

        self.all_quiz_questions = self.load_quiz_questions()
        self.current_quiz_question = None

        self.question_label = tk.Label(
            self.root_window, text="", font=("Arial", 14), wraplength=450, justify="left"
        )
        self.question_label.pack(pady=20)

        self.selected_answer_option = tk.StringVar()
        self.answer_option_buttons = {}

        for answer_option_key in ['a', 'b', 'c', 'd']:
            answer_button = tk.Radiobutton(
                self.root_window,
                text="",
                variable=self.selected_answer_option,
                value=answer_option_key,
                font=("Arial", 12),
                anchor="w",
                justify="left"
            )
            answer_button.pack(fill='x', padx=50, pady=2)
            self.answer_option_buttons[answer_option_key] = answer_button

        self.submit_button = tk.Button(
            self.root_window, text="Submit Answer", command=self.check_user_answer
        )
        self.submit_button.pack(pady=10)

        self.quit_button = tk.Button(
            self.root_window, text="❌ Exit Quiz", command=self.root_window.quit
        )
        self.quit_button.pack()

        self.load_random_quiz_question()

    def load_quiz_questions(self):
        if not os.path.exists(self.QUIZ_FILENAME) or os.stat(self.QUIZ_FILENAME).st_size == 0:
            return []
        with open(self.QUIZ_FILENAME, 'r', encoding='utf-8') as quiz_file:
            return [json.loads(line) for line in quiz_file if line.strip()]

    def load_random_quiz_question(self):
        if not self.all_quiz_questions:
            messagebox.showinfo("Done", "No more questions available.")
            self.root_window.quit()
            return

        self.current_quiz_question = random.choice(self.all_quiz_questions)
        self.question_label.config(text=self.current_quiz_question["question"])

        for answer_option_key, answer_option_text in self.current_quiz_question["choices"].items():
            self.answer_option_buttons[answer_option_key].config(
                text=f"{answer_option_key.upper()}) {answer_option_text}"
            )

        self.selected_answer_option.set(None)

    def check_user_answer(self):
        user_selected_option = self.selected_answer_option.get()

        if not user_selected_option:
            messagebox.showwarning("No Answer", "Please select an answer before submitting.")
            return

        correct_answer_key = self.current_quiz_question["answer"]
        if user_selected_option == correct_answer_key:
            messagebox.showinfo("Correct!", "🎉 That's the correct answer!")
        else:
            correct_answer_text = self.current_quiz_question["choices"][correct_answer_key]
            messagebox.showerror(
                "Incorrect",
                f"❌ The correct answer was: {correct_answer_key.upper()}) {correct_answer_text}"
            )

        self.all_quiz_questions.remove(self.current_quiz_question)
        self.load_random_quiz_question()

if __name__ == "__main__":
    root_window = tk.Tk()
    quiz_app_instance = QuizAnsweringApp(root_window)
    root_window.mainloop()
