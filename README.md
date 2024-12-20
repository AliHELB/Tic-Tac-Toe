# Tic-Tac-Toe Web Application

This project is a web-based implementation of the classic Tic-Tac-Toe game built using the Django framework. It features user authentication, customizable game settings, and real-time gameplay updates for an engaging user experience.

## Features

### Gameplay
- Create and join public or private Tic-Tac-Toe games.
- Customizable grid sizes and winning conditions.
- Real-time updates via AJAX for a seamless experience.
- Support for forfeits, draws, and winner determination.

### User Management
- Registration, login, and logout functionality.
- User profiles with customizable avatars and game symbols.
- Profile update options with image resizing.

### Interface
- Clean and responsive design using Bootstrap.
- Interactive game board with dynamic updates.
- Easy navigation between features.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AliHELB/Tic-Tac-Toe.git
   cd Tic-Tac-Toe
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:8000`.

## Requirements
- Python 3.8 or higher
- Django 3.2 or higher
- Pillow for image handling
- Bootstrap (via Django crispy forms)

## Folder Structure
- **`morpion/`**: Contains the logic for the Tic-Tac-Toe game.
- **`users/`**: Manages user profiles and authentication.
- **`templates/`**: HTML templates for the app.
- **`static/`**: Static files like CSS and JavaScript.

## Acknowledgements
- [Django Framework](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/) for styling.

Enjoy the game and have fun!
