import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from tkinter.scrolledtext import ScrolledText
from fpdf import FPDF
from textblob import TextBlob
import datetime

class DeskTopTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeskTop Text 2025")
        self.root.geometry("1000x650")

        self.word_goal = 0
        self.dark_mode = False
        self.typewriter_mode = False
        self.in_focus_mode = False
        self.snippets = {
            "Signature": "Best regards,\nYour Name",
            "Greeting": "Dear Sir/Madam,\n\n",
            "Thank You": "Thank you for your time and consideration.",
        }
        self.templates = {
            "Letter": "Dear [Recipient],\n\n[Your message here]\n\nSincerely,\n[Your Name]",
            "Essay": "Title: [Your Title Here]\n\nIntroduction:\n[Start your essay here...]",
            "Report": "Report Title: [Title Here]\n\nExecutive Summary:\n[Summary here...]",
        }
        self.versions = []

        self.build_menu()
        self.build_editor()

    def build_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Export as PDF", command=self.export_pdf)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Bold", command=self.make_bold)
        edit_menu.add_command(label="Italic", command=self.make_italic)
        edit_menu.add_command(label="Underline", command=self.make_underline)
        edit_menu.add_command(label="Text Color", command=self.choose_color)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # View Menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Enter Focus Mode", command=self.toggle_focus_mode)
        view_menu.add_command(label="Exit Focus Mode", command=self.exit_focus_mode)
        view_menu.add_command(label="Toggle Typewriter Mode", command=self.toggle_typewriter_mode)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        view_menu.add_command(label="Change Theme", command=self.change_theme)
        menubar.add_cascade(label="View", menu=view_menu)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Set Word Goal", command=self.set_word_goal)
        tools_menu.add_command(label="Analyze Mood", command=self.analyze_mood)
        tools_menu.add_command(label="Insert Snippet", command=self.insert_snippet)
        tools_menu.add_command(label="Insert Template", command=self.insert_template)
        tools_menu.add_command(label="AI Text Generator", command=self.ai_generator)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About DeskTop Text 2025", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def build_editor(self):
        self.text_area = ScrolledText(self.root, wrap=tk.WORD, font=("Segoe UI", 12), undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<KeyRelease>", self.update_word_count)

        self.status_bar = tk.Label(self.root, text="Words: 0", anchor=tk.W, bg="#f2f2f2")
        self.status_bar.pack(fill=tk.X)

        self.auto_save_version()

    # ---------- File Functions ----------
    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.auto_save_version()

    def open_file(self):
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f.read())

    def export_pdf(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            content = self.text_area.get(1.0, tk.END).split("\n")
            for line in content:
                pdf.cell(200, 10, txt=line, ln=1)
            pdf.output(file)

    # ---------- Edit ----------
    def make_bold(self):
        try:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
            self.text_area.tag_config("bold", font=("Segoe UI", 12, "bold"))
        except:
            pass

    def make_italic(self):
        try:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
            self.text_area.tag_config("italic", font=("Segoe UI", 12, "italic"))
        except:
            pass

    def make_underline(self):
        try:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
            self.text_area.tag_config("underline", font=("Segoe UI", 12, "underline"))
        except:
            pass

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            try:
                self.text_area.tag_add("color", "sel.first", "sel.last")
                self.text_area.tag_config("color", foreground=color)
            except:
                pass

    # ---------- View ----------
    def toggle_focus_mode(self):
        if not self.in_focus_mode:
            self.status_bar.pack_forget()
            self.in_focus_mode = True

    def exit_focus_mode(self):
        if self.in_focus_mode:
            self.status_bar.pack(fill=tk.X)
            self.in_focus_mode = False

    def toggle_typewriter_mode(self):
        self.typewriter_mode = not self.typewriter_mode
        if self.typewriter_mode:
            self.text_area.yview_moveto(0.4)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.text_area.config(bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        else:
            self.text_area.config(bg="white", fg="black", insertbackground="black")

    def change_theme(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(bg=color)

    # ---------- Tools ----------
    def set_word_goal(self):
        goal = simpledialog.askinteger("Word Goal", "Set a word goal:")
        if goal:
            self.word_goal = goal
            self.update_word_count()

    def update_word_count(self, event=None):
        content = self.text_area.get(1.0, tk.END)
        words = len(content.split())
        self.status_bar.config(text=f"Words: {words} / Goal: {self.word_goal}" if self.word_goal else f"Words: {words}")

    def analyze_mood(self):
        content = self.text_area.get(1.0, tk.END)
        blob = TextBlob(content)
        polarity = blob.sentiment.polarity
        mood = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        messagebox.showinfo("Mood Analyzer", f"Overall Mood: {mood} (Polarity: {polarity:.2f})")

    def insert_snippet(self):
        choice = simpledialog.askstring("Insert Snippet", f"Available: {', '.join(self.snippets.keys())}\nEnter snippet name:")
        if choice and choice in self.snippets:
            self.text_area.insert(tk.INSERT, self.snippets[choice])

    def insert_template(self):
        choice = simpledialog.askstring("Insert Template", f"Available: {', '.join(self.templates.keys())}\nEnter template name:")
        if choice and choice in self.templates:
            self.text_area.insert(tk.INSERT, self.templates[choice])

    def ai_generator(self):
        prompt = simpledialog.askstring("AI Text Generator", "Enter your prompt:")
        if prompt:
            generated = f"[AI Response to: '{prompt}']\nThis is a placeholder response.\n"
            self.text_area.insert(tk.INSERT, generated)

    def auto_save_version(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = self.text_area.get(1.0, tk.END)
        self.versions.append((timestamp, content))
        if len(self.versions) > 10:
            self.versions.pop(0)

    def show_about(self):
        messagebox.showinfo("About", "DeskTop Text 2025\n© 1997–2025 NeTT Systems")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeskTopTextApp(root)
    root.mainloop()
