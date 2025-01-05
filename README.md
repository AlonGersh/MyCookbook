# MyCookbook

![mycookbook-high-resolution-logo - Copy](https://github.com/user-attachments/assets/25de0d9d-e336-456b-9006-bffb237e16b5)

## What is MyCookbook?
In today's digital age, with recipes flooding the internet from blogs, social media, and other platforms, keeping track of favorite recipes can be a daunting task. For cooking enthusiasts, the challenge lies in storing and organizing these recipes in a way that makes them easily accessible when needed.

MyCookbook was created to address that need — a simple and intuitive tool to organize, store, and manage recipes in a personal digital cooking book. It allows users to categorize their recipes, view them easily, annotate with personal comments, and navigate through their collection effortlessly — making the cooking experience more enjoyable and organized.

## How It Works?
The Recipe Organizer App is built using Python and Tkinter, with a simple graphical user interface (GUI) to make it user-friendly.

### Features:
1. **Add a Recipe**: Users can add new recipes by providing the recipe name, ingredients, instructions, an image (via URL), and a link to a video tutorial (if available)
  
2. **Organize Recipes**: Recipes can be categorized into categories such as: Desserts, Soups, Salads, etc. The app will display the recipe under the chosen category

3. **View and Edit Recipes**: When a recipe is selected, users can view the full recipe with its instructions, image, and video link. A "Edit" option allows users to update existing recipes

4. **Comments**: In the recipe page users can add personal comments to each recipe, which can be useful for noting modifications or favorite variations

5. **Recipe Export**: Users can export a recipe to a text file if they would like a hard copy. The exported file will include a copyright mark acknowledging the recipe's author


## Requirements
- Python 3 or higher version recommended

### Dependencies
- `tkinter`: (typically comes pre-installed with Python): Core module for creating the GUI
- `os`: For file and directory operations
- `json`: For handling JSON data
- `io. BytesIO`: For working with binary data streams (used to handle image data)
- `Pillow`: Provides the Image and ImageTk modules for working with images
- `tkinter`: Used for themed widgets in the GUI
- `requests`: Used for making HTTP requests to fetch images from URLs

  
## Tests
Will be updated

  
## Installation
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/AlonGersh/MyCookbook.git 

3. Navigate to the directory where the code is located.
   ```bash
   cd MyCookbook

4. Install the required libraries (if not already installed):
   ```bash
    pip install pillow

5. Run the app:
   ```bash
   python MyCookbook.py

*This project was developed as part of the Python programming course at the Weizmann Institute (November 2024).
