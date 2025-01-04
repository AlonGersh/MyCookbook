# MyCookbook - bring order to the chaos of collecting online recipes

## Background

In today's digital age, with recipes flooding the internet from blogs, social media, and other platforms, keeping track of favorite recipes can be a daunting task. For cooking enthusiasts, the challenge lies in storing and organizing these recipes in a way that makes them easily accessible when needed.

MyCookbook was created to address that need—a simple and intuitive tool to organize, store, and manage recipes in a personal digital cooking book. It allows users to categorize their recipes, view them easily, annotate with personal comments, and navigate through their collection effortlessly, making your cooking experience more enjoyable and organized.

## How It Works
The Recipe Organizer App is built using Python and Tkinter, with a simple graphical user interface (GUI) to make it user-friendly. Here’s a breakdown of its main features:

- **Add Recipes**: Users can add new recipes by providing the recipe name, ingredients, instructions, an image (via URL), and a link to a video tutorial (if available).
  
- **Recipe Categories**: Recipes can be categorized into pre-set categories such as: Desserts, Soups, Salads, etc. The user can select the category while adding a recipe, and the app will display the recipe under the chosen category.

- **View and Edit Recipes**: When a recipe is selected, users can view the full recipe with its instructions, image (if provided), and video link (if provided). A "Edit" option allows users to update existing recipes.

- **Comments Section**: In the recipe page users can add personal comments to each recipe, which can be useful for noting modifications or favorite variations.

## Features Overview
1. **Add a Recipe**: Fill out the recipe name, category, instructions, optional video link, and image URL.
2. **Organize Recipes**: Categorize recipes under labels such as "Main," "Dessert," and "Bread."
3. **View Recipe**: See the details of a selected recipe, including the instructions, image, and video link.
4. **Edit Recipe**: Update the recipe information or image.
5. **Comments**: Add notes or comments to each recipe for personal use.


### Requirements
- Python 3.x
- Tkinter (typically comes pre-installed with Python)
- PIL (Python Imaging Library) for handling images

  
## Installation
To install and run the app on your machine, follow these steps:


### Steps to Install
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/recipe-organizer.git

2. Navigate to the directory where the code is located.
   ```bash
   cd MyCookbook

3. Install the required libraries (if not already installed):
   ```bash
    pip install pillow

4. Run the app:
   ```bash
   python MyCookbook.py
