import tkinter as tk
from tkinter import messagebox
import json
import os

class QuizFileHandler:
    file_name = "quiz_generator.txt"

    @classmethod
    def load_quiz_data(cls):
        if not os.path.exists(cls.file_name) or os.stat(cls.file_name).st_size == 0:
            return []
        with open(cls.file_name, 'r', encoding='utf-8') as file_handle:
            return [json.loads(line) for line in file_handle if line.strip()]

    @classmethod
    def save_question(cls, question_data):
        with open(cls.file_name, 'a', encoding='utf-8') as file_handle:
            file_handle.write(json.dumps(question_data, ensure_ascii=False) + "\n")

    @classmethod
    def overwrite_all_questions(cls, questions_list):
        with open(cls.file_name, 'w', encoding='utf-8') as file_handle:
            for question_data in questions_list:
                file_handle.write(json.dumps(question_data, ensure_ascii=False) + "\n")


class QuizApp:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("\U0001F9E0 Quiz Generator Program")
        self.root_window.geometry("500x500")
        self.root_window.resizable(False, False)

        self.quiz_data = []

        self.frames = {}
        for frame_class in (MainMenu, CreateQuiz, ManageQuiz):
            frame_instance = frame_class(self.root_window, self)
            self.frames[frame_class] = frame_instance
            frame_instance.place(relwidth=1, relheight=1)

        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def refresh_quiz_data(self):
        self.quiz_data = QuizFileHandler.load_quiz_data()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="\U0001F9E0 QUIZ GENERATOR", font=("Arial", 18)).pack(pady=30)
        tk.Button(self, text="\U0001F4DA Create Quiz", width=20, command=lambda: controller.show_frame(CreateQuiz)).pack(pady=10)
        tk.Button(self, text="⚒️ Manage Questions", width=20, command=lambda: controller.show_frame(ManageQuiz)).pack(pady=10)
        tk.Button(self, text="❌ Exit", width=20, command=self.controller.root_window.destroy).pack(pady=10)


class CreateQuiz(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="⚒️ Create a Quiz Question", font=("Arial", 14)).pack(pady=10)

        self.entry_question = self.create_labeled_entry("Question:")
        self.entry_choice_a = self.create_labeled_entry("Choice A:")
        self.entry_choice_b = self.create_labeled_entry("Choice B:")
        self.entry_choice_c = self.create_labeled_entry("Choice C:")
        self.entry_choice_d = self.create_labeled_entry("Choice D:")

        self.correct_answer_var = tk.StringVar()
        tk.Label(self, text="Correct Answer:", font=('Arial', 12)).pack(pady=5)
        for choice_key in ['a', 'b', 'c', 'd']:
            tk.Radiobutton(self, text=f"{choice_key.upper()}", variable=self.correct_answer_var, value=choice_key).pack(anchor="w", padx=100)

        tk.Button(self, text="✅ Save Question", command=self.save_question_to_file, bg="green", fg="white").pack(pady=10)
        tk.Button(self, text="⚒️ Manage Questions", command=lambda: controller.show_frame(ManageQuiz)).pack(pady=2)
        tk.Button(self, text="↩️ Return to Menu", command=lambda: controller.show_frame(MainMenu)).pack(pady=5)

    def create_labeled_entry(self, label_text):
        tk.Label(self, text=label_text).pack()
        entry_field = tk.Entry(self, width=50)
        entry_field.pack(pady=2)
        return entry_field

    def save_question_to_file(self):
        question_text = self.entry_question.get().strip()
        choice_a = self.entry_choice_a.get().strip()
        choice_b = self.entry_choice_b.get().strip()
        choice_c = self.entry_choice_c.get().strip()
        choice_d = self.entry_choice_d.get().strip()
        correct_answer = self.correct_answer_var.get()

        if not all([question_text, choice_a, choice_b, choice_c, choice_d, correct_answer]):
            messagebox.showwarning("Missing Info", "Please fill in all fields and select the correct answer.")
            return

        question_data = {
            "question": question_text,
            "choices": {"a": choice_a, "b": choice_b, "c": choice_c, "d": choice_d},
            "answer": correct_answer
        }

        QuizFileHandler.save_question(question_data)
        messagebox.showinfo("Saved", "Question added successfully.")
        self.clear_input_fields()

    def clear_input_fields(self):
        self.entry_question.delete(0, tk.END)
        self.entry_choice_a.delete(0, tk.END)
        self.entry_choice_b.delete(0, tk.END)
        self.entry_choice_c.delete(0, tk.END)
        self.entry_choice_d.delete(0, tk.END)
        self.correct_answer_var.set(None)


class ManageQuiz(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="\U0001F4CB Manage Questions", font=('Arial', 14)).pack(pady=10)

        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self.container)
        self.scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(self.container, yscrollcommand=self.scrollbar.set, width=80)
        self.listbox.pack(padx=10, pady=10, fill='both', expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        tk.Button(self, text="✏️ Edit Selected", command=self.edit_selected_question).pack(pady=5)
        tk.Button(self, text="\U0001F5D1️ Delete Selected", command=self.delete_selected_question).pack(pady=5)
        tk.Button(self, text="↩️ Back to Create", command=lambda: controller.show_frame(CreateQuiz)).pack(pady=10)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.refresh_question_list()

    def refresh_question_list(self):
        self.listbox.delete(0, tk.END)
        self.quiz_data = QuizFileHandler.load_quiz_data()
        for index, question_entry in enumerate(self.quiz_data):
            question_text = question_entry['question']
            self.listbox.insert(tk.END, f"{index + 1}. {question_text}")

    def edit_selected_question(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_question_data = self.quiz_data.pop(selected_index)
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a question to edit.")
            return

        create_quiz_frame = self.controller.frames[CreateQuiz]
        create_quiz_frame.entry_question.delete(0, tk.END)
        create_quiz_frame.entry_question.insert(0, selected_question_data['question'])

        create_quiz_frame.entry_choice_a.delete(0, tk.END)
        create_quiz_frame.entry_choice_a.insert(0, selected_question_data['choices']['a'])

        create_quiz_frame.entry_choice_b.delete(0, tk.END)
        create_quiz_frame.entry_choice_b.insert(0, selected_question_data['choices']['b'])

        create_quiz_frame.entry_choice_c.delete(0, tk.END)
        create_quiz_frame.entry_choice_c.insert(0, selected_question_data['choices']['c'])

        create_quiz_frame.entry_choice_d.delete(0, tk.END)
        create_quiz_frame.entry_choice_d.insert(0, selected_question_data['choices']['d'])

        create_quiz_frame.correct_answer_var.set(selected_question_data['answer'])

        QuizFileHandler.overwrite_all_questions(self.quiz_data)
        self.controller.show_frame(CreateQuiz)

    def delete_selected_question(self):
        try:
            selected_index = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a question to delete.")
            return

        confirm_delete = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
        if confirm_delete:
            self.quiz_data.pop(selected_index)
            QuizFileHandler.overwrite_all_questions(self.quiz_data)
            self.refresh_question_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
