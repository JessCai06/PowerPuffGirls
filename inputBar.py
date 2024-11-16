from cmu_graphics import *

def onAppStart(app):
    app.input = ""  # User input
    app.clipboard = ""  # Simulated clipboard
    app.screen = 'input'  # Start with the input screen
    app.calculated = False  # Whether input submission is completed
    app.error = False  # Tracks invalid input

def onKeyPress(app, key):
    if app.screen == 'input':
        app.error = False  # Reset error state if a new key is pressed

        # Handle backspace
        if key == 'backspace' and app.input:
            app.input = app.input[:-1]
        # Handle copy (Ctrl+C or Command+C)
        elif key == 'ctrl+c' or key == 'command+c':
            app.clipboard = app.input
        # Handle paste (Ctrl+V or Command+V)
        elif key == 'ctrl+v' or key == 'command+v':
            app.input += app.clipboard
        # Handle alphanumeric characters and basic math operators
        elif key.isalnum() or key in ['+', '-', ' ']:
            app.input += key
        # Trigger action on Enter
        elif key == 'enter':
            validateAndProceed(app)

def handleAnalyzeClick(app):
    if app.screen == 'input':
        validateAndProceed(app)

def validateAndProceed(app):
    """Validates user input and transitions to the next screen."""
    if app.input.strip():  # Ensure input is not empty
        app.calculated = True
        app.screen = 'categories'
    else:
        app.error = True  # Flag input as invalid

def drawInputScreen(app):
    # Background and Title
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('User Input Screen', 20, 30, size=36, bold=True, fill='white', align='left', font='impact')

    # Input Bar
    drawRect(100, 300, 600, 50, fill='white', border='gray')  # Input box background
    drawLabel(app.input if app.input else "Type your input here...", 110, 325, size=18, align='left',
              fill='black' if app.input else 'gray', font='verdana')

    # Error Message
    if app.error:
        drawLabel("Input cannot be empty!", app.width / 2, 400, size=16, fill='red', font='verdana')

    # Analyze Button
    drawRect(300, 500, 200, 50, fill='lavender')
    drawLabel('Analyze', 400, 525, size=24, fill='white', font='verdana')

def handleAnalyzeMousePress(app, mouseX, mouseY):
    if 300 <= mouseX <= 500 and 500 <= mouseY <= 550:  # Analyze button click
        validateAndProceed(app)

def drawCategoryScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('Category Selection Screen', 20, 30, size=36, bold=True, fill='white', align='left', font='impact')
    drawLabel(f'You entered: {app.input}', app.width / 2, app.height / 2, size=24, fill='white', font='verdana')

############################################################
# Shared Event Handlers
############################################################

def redrawAll(app):
    if app.screen == 'input':
        drawInputScreen(app)
    elif app.screen == 'categories':
        drawCategoryScreen(app)

def onMousePress(app, mouseX, mouseY):
    if app.screen == 'input':
        handleAnalyzeMousePress(app, mouseX, mouseY)

############################################################
# Main
############################################################

def main():
    runApp(width=800, height=1000)

main()
