import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import json
import requests
from io import BytesIO
import webbrowser
from functools import partial

if not os.path.exists("data"):
    os.makedirs("data")

RECIPE_FILE = "data/recipes.json"

# Load recipes from the JSON file
def load_recipes():
    if os.path.exists(RECIPE_FILE):
        with open(RECIPE_FILE, "r") as file:
            return json.load(file)
    return []

# Save recipes to the JSON file
def save_recipes(recipes):
    with open(RECIPE_FILE, "w") as file:
        json.dump(recipes, file, indent=4)

recipes = load_recipes()

class RecipeWindow:
    def __init__(self, app, recipe_index=None):
        self.app = app
        self.recipe_index = recipe_index
        self.window = tk.Toplevel()
        self.window.title("Add Recipe" if recipe_index is None else "Edit Recipe")

        # Fields for the recipe form
        fields = [
            ("Recipe Name:", "name", tk.Entry, {}),
            ("Category:", "category", ttk.Combobox, {"values": self.app.categories, "state": "readonly"}),
            ("Ingredients:", "ingredients", tk.Text, {"width": 30, "height": 5, "wrap": tk.WORD}),
            ("Instructions:", "instructions", tk.Text, {"width": 30, "height": 10, "wrap": tk.WORD}),
            ("Recipe link:", "video_link", tk.Entry, {}),
            ("Image:", "image", tk.Entry, {}),
            ("Comments:", "comments", tk.Text, {"width": 30, "height": 5, "wrap": tk.WORD}),
        ]

        # Create and place widgets for each field
        self.entries = {}
        for i, (label_text, field_name, widget_type, kwargs) in enumerate(fields):
            ttk.Label(self.window, text=label_text).grid(row=i, column=0, padx=10, pady=5)
            entry = widget_type(self.window, **kwargs)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field_name] = entry

        # Load recipe data if editing
        if recipe_index is not None:
            self.load_recipe(recipes[recipe_index])

        # "Save Recipe" button
        ttk.Button(self.window, text="Save Recipe", command=self.save_recipe).grid(row=len(fields), column=1, pady=10)

    def load_recipe(self, recipe):
        # Populate form fields with recipe data
        for field, entry in self.entries.items():
            if field == "comments":
                if isinstance(recipe[field], list):
                    entry.insert(tk.END, "\n".join(recipe[field]))
                else:
                    entry.insert(tk.END, recipe[field])
            elif field == "category":
                entry.set(recipe[field])
            else:
                entry.insert(tk.END, recipe[field])

    def save_recipe(self):
        # Collect data from form fields
        recipe_data = {}
        for field, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                recipe_data[field] = entry.get("1.0", tk.END).strip()
            else:
                recipe_data[field] = entry.get().strip()

        # Validate recipe name
        if not recipe_data["name"]:
            messagebox.showerror("Error", "Recipe name is required.")
            return

        # Add or update recipe in the list
        if self.recipe_index is None:
            recipes.append(recipe_data)
        else:
            recipes[self.recipe_index] = recipe_data

        # Save recipes and update the UI
        save_recipes(recipes)
        self.app.update_recipe_list()
        self.window.destroy()
        messagebox.showinfo("Success", "Recipe saved successfully.")

class MyCookBook:
    def __init__(self, root):
        self.root = root
        self.root.title("MyCookBook")

        # Define recipe categories
        self.categories = ["All recipes", "Desserts", "Bread", "Soups", "Salads", "Pasta", "Main Dishes"]
        self.filtered_category = "All recipes"

        # Create the GUI widgets
        self.create_widgets()

    def create_widgets(self):
        # Category filter buttons
        self.category_frame = ttk.Frame(self.root)
        self.category_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        for category in self.categories:
            button = ttk.Button(self.category_frame, text=category, command=partial(self.filter_recipes, category))
            button.pack(side=tk.LEFT, padx=5)

        # Recipe list with scrollbar
        self.recipe_list_frame = ttk.Frame(self.root)
        self.recipe_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.recipe_listbox = tk.Listbox(self.recipe_list_frame, height=20, width=40)
        self.recipe_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.recipe_listbox.bind("<Double-1>", self.view_recipe)

        self.scrollbar = ttk.Scrollbar(self.recipe_list_frame, orient=tk.VERTICAL, command=self.recipe_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.config(yscrollcommand=self.scrollbar.set)

        # Action buttons
        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        buttons = [
            ("Add Recipe", self.add_recipe),
            ("View Recipe", self.view_recipe),
            ("Edit Recipe", self.edit_recipe),
            ("Delete Recipe", self.delete_recipe),
            ("Export Recipe", self.export_recipe),
        ]

        for text, command in buttons:
            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.pack(pady=10)

        # Populate the recipe list
        self.update_recipe_list()

    def filter_recipes(self, category):
        # Filter recipes by category
        self.filtered_category = category
        self.update_recipe_list()

    def update_recipe_list(self):
        # Update the listbox with filtered recipes
        self.recipe_listbox.delete(0, tk.END)
        filtered_recipes = recipes if self.filtered_category == "All recipes" else [r for r in recipes if r["category"] == self.filtered_category]
        for recipe in filtered_recipes:
            self.recipe_listbox.insert(tk.END, recipe["name"])

    def add_recipe(self):
        # Open window to add a new recipe
        RecipeWindow(self)

    def view_recipe(self, event=None):
        # Open window to view the selected recipe
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe_index = self.get_recipe_index(selected_index[0])
            ViewRecipeWindow(self, recipe_index)
        else:
            messagebox.showinfo("Info", "Please select a recipe to view")

    def edit_recipe(self):
        # Open window to edit the selected recipe
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe_index = self.get_recipe_index(selected_index[0])
            RecipeWindow(self, recipe_index)
        else:
            messagebox.showinfo("Info", "Please select a recipe to edit")

    def delete_recipe(self):
        # Delete the selected recipe
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe_index = self.get_recipe_index(selected_index[0])
            del recipes[recipe_index]
            save_recipes(recipes)
            self.update_recipe_list()
            messagebox.showinfo("Success", "Recipe deleted successfully")
        else:
            messagebox.showinfo("Info", "Please select a recipe to delete")

    def export_recipe(self):
        # Export the selected recipe to a text file
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe_index = self.get_recipe_index(selected_index[0])
            recipe = recipes[recipe_index]
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Recipe: {recipe['name']}\n\n")
                    file.write(f"Category: {recipe['category']}\n\n")
                    file.write(f"Instructions:\n{recipe['instructions']}\n\n")
                    file.write(f"Ingredients:\n{recipe['ingredients']}\n\n")
                    file.write(f"Recipe link: {recipe['video_link']}\n\n")
                    file.write(f"Image: {recipe['image']}\n\n")
                    file.write("Comments:\n")
                    if isinstance(recipe["comments"], list):
                        file.write("\n".join(f"- {comment}" for comment in recipe["comments"]) + "\n")
                    else:
                        file.write(f"- {recipe['comments']}\n")

                messagebox.showinfo("Success", f"Recipe exported to {file_path}")
        else:
            messagebox.showinfo("Info", "Please select a recipe to export")

    def get_recipe_index(self, selected_index):
        # Get the index of the selected recipe, accounting for category filtering
        if self.filtered_category == "All recipes":
            return selected_index
        else:
            filtered_recipes = [r for r in recipes if r["category"] == self.filtered_category]
            return recipes.index(filtered_recipes[selected_index])

class ViewRecipeWindow:
    def __init__(self, app, recipe_index):
        self.app = app
        self.recipe = recipes[recipe_index]
        self.recipe_index = recipe_index

        self.window = tk.Toplevel()
        self.window.title(self.recipe["name"])

        # Create a scrollable canvas for recipe details
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Display recipe details
        ttk.Label(self.scrollable_frame, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(self.scrollable_frame, text=self.recipe["category"]).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.scrollable_frame, text="Ingredients:").grid(row=1, column=0, padx=10, pady=5, sticky="ne")
        ingredients_label = ttk.Label(self.scrollable_frame, text=self.recipe["ingredients"], wraplength=400, justify="left")
        ingredients_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.scrollable_frame, text="Instructions:").grid(row=2, column=0, padx=10, pady=5, sticky="ne")
        instructions_label = ttk.Label(self.scrollable_frame, text=self.recipe["instructions"], wraplength=400, justify="left")
        instructions_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.scrollable_frame, text="Recipe link:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        video_link = self.recipe["video_link"]
        if video_link:
            clickable_link = tk.Label(self.scrollable_frame, text=video_link, fg="blue", cursor="hand2")
            clickable_link.grid(row=3, column=1, padx=10, pady=5, sticky="w")
            clickable_link.bind("<Button-1>", lambda e, url=video_link: webbrowser.open(url))

        ttk.Label(self.scrollable_frame, text="Image:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        image_path = self.recipe["image"]
        if image_path:
            try:
                if image_path.startswith(('http://', 'https://')):
                    response = requests.get(image_path)
                    img = Image.open(BytesIO(response.content))
                else:
                    img = Image.open(image_path)
                
                img.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(self.scrollable_frame, image=photo)
                img_label.image = photo
                img_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
            except Exception as e:
                ttk.Label(self.scrollable_frame, text=f"Error loading image: {str(e)}").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        else:
            ttk.Label(self.scrollable_frame, text="No image available").grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(self.scrollable_frame, text="Comments:").grid(row=5, column=0, padx=10, pady=5, sticky="ne")
        comments_text = self.recipe["comments"] if isinstance(self.recipe["comments"], str) else "\n".join(self.recipe["comments"])
        comments_label = ttk.Label(self.scrollable_frame, text=comments_text, wraplength=400, justify="left")
        comments_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Export button
        export_button = ttk.Button(self.window, text="Export txt file", command=self.export_recipe)
        export_button.grid(row=6, column=1, pady=10)

    def export_recipe(self):
        # Export recipe to a text file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Recipe: {self.recipe['name']}\n\n")
                file.write(f"Category: {self.recipe['category']}\n\n")
                file.write(f"Instructions:\n{self.recipe['instructions']}\n\n")
                file.write(f"Ingredients:\n{self.recipe['ingredients']}\n\n")
                file.write(f"Recipe link: {self.recipe['video_link']}\n\n")
                file.write(f"Image: {self.recipe['image']}\n\n")
                file.write("Comments:\n")
                for comment in self.recipe['comments']:
                    file.write(f"- {comment}\n")
            messagebox.showinfo("Success", f"Recipe exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyCookBook(root)
    root.mainloop()
