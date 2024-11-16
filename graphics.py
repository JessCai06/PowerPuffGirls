from cmu_graphics import *
import random

def onAppStart(app):
    # Shared state
    app.width = 800
    app.height = 1000
    app.screen = 'start'  # Initial screen
    app.soundURL = ""
    app.selectedCategories = []
    app.categories = [
        "Tempo", "Beats per Minute", "Duration", "Tone", "Key",
        "Dominant Timbres", "Rhythms", "Harmony", "Melody", "Pitch",
        "Volume", "Chords", "Structure", "Dynamics", "Mood",
        "Genre", "Instrumentation", "Phrasing", "Articulation", "Texture"
    ]
    app.categoryColors = [
        "lightpink", "lavender", "lightblue", "thistle", "plum", "powderblue"
    ]
    app.promptingSoundURL = True

############################################################
# Helper Functions for Rounded Buttons
############################################################

def drawRoundedRect(x, y, width, height, fill):
    """Draw a rounded rectangle with circles at each corner."""
    cornerRadius = min(width, height) // 4
    drawRect(x + cornerRadius, y, width - 2 * cornerRadius, height, fill=fill)  # Middle rectangle
    drawRect(x, y + cornerRadius, width, height - 2 * cornerRadius, fill=fill)  # Vertical bars
    drawCircle(x + cornerRadius, y + cornerRadius, cornerRadius, fill=fill)  # Top-left corner
    drawCircle(x + width - cornerRadius, y + cornerRadius, cornerRadius, fill=fill)  # Top-right corner
    drawCircle(x + cornerRadius, y + height - cornerRadius, cornerRadius, fill=fill)  # Bottom-left corner
    drawCircle(x + width - cornerRadius, y + height - cornerRadius, cornerRadius, fill=fill)  # Bottom-right corner

def getTextWidth(text, fontSize):
    """Estimate text width based on character count and font size."""
    return len(text) * fontSize * 0.6

############################################################
# Progress Bar and Navigation Helper
############################################################

def drawProgressBar(app):
    # Progress bar at the bottom
    barY = app.height - 50
    dotRadius = 10
    gap = 60
    x1 = app.width / 2 - gap
    x2 = app.width / 2
    x3 = app.width / 2 + gap

    # Draw connecting lines
    if app.screen in ['categories', 'analyze']:
        drawLine(x1, barY, x2, barY, fill='white', lineWidth=2)
    if app.screen == 'analyze':
        drawLine(x2, barY, x3, barY, fill='white', lineWidth=2)

    # Draw dots
    drawCircle(x1, barY, dotRadius + (5 if app.screen in ['start', 'categories', 'analyze'] else 0), fill='white')
    drawCircle(x2, barY, dotRadius + (5 if app.screen in ['categories', 'analyze'] else 0), fill='white')
    drawCircle(x3, barY, dotRadius + (5 if app.screen == 'analyze' else 0), fill='white')

    # Draw arrows
    arrowSize = 20
    if app.screen != 'start':  # Show left arrow
        drawLabel('<', 100, barY, size=arrowSize, fill='white', font='verdana')
    if app.screen != 'analyze':  # Show right arrow
        drawLabel('>', app.width - 100, barY, size=arrowSize, fill='white', font='verdana')

def handleProgressBarClick(app, mouseX, mouseY):
    barY = app.height - 50
    if 80 <= mouseX <= 120 and barY - 20 <= mouseY <= barY + 20:  # Left arrow
        if app.screen == 'categories':
            app.screen = 'start'
        elif app.screen == 'analyze':
            app.screen = 'categories'
    elif app.width - 120 <= mouseX <= app.width - 80 and barY - 20 <= mouseY <= barY + 20:  # Right arrow
        if app.screen == 'start':
            app.screen = 'categories'
        elif app.screen == 'categories':
            app.screen = 'analyze'

############################################################
# Start Screen
############################################################

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('Input Sound URL', 20, 30, size=36, bold=True, fill='white', align='left', font='impact')
    drawLabel('Enter a sound file URL (http or cmu://):', app.width / 2, 200, size=24, fill='white', align='center', font='verdana')
    drawLabel(app.soundURL, app.width / 2, 250, size=20, fill='white', align='center', font='verdana')
    drawRoundedRect(300, 400, 200, 50, fill='lavender')
    drawLabel('Next', 400, 425, size=24, fill='white', font='verdana')
    drawProgressBar(app)

def handleStartKeyPress(app, key):
    if app.promptingSoundURL:
        if key == "Enter":
            app.promptingSoundURL = False  # Finish URL input
        elif key == "Backspace":
            app.soundURL = app.soundURL[:-1]
        else:
            app.soundURL += key

def handleStartMousePress(app, mouseX, mouseY):
    if 300 <= mouseX <= 500 and 400 <= mouseY <= 450:  # Next button
        app.screen = 'categories'
    handleProgressBarClick(app, mouseX, mouseY)

############################################################
# Category Selection Screen
############################################################

def drawCategoryScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('Select Categories', 20, 30, size=36, bold=True, fill='white', align='left', font='impact')
    y = 100
    x = 50
    maxRowWidth = app.width - 50

    for i, category in enumerate(app.categories):
        textWidth = getTextWidth(category, 20) + 40  # Button width based on text
        color = random.choice(app.categoryColors)

        # Adjust row when exceeding the width
        if x + textWidth > maxRowWidth:
            x = 50
            y += 70

        drawRoundedRect(x, y, textWidth, 50, fill=color)
        drawLabel(category, x + textWidth / 2, y + 25, size=20, fill='black', font='verdana')
        x += textWidth + 20

    drawRoundedRect(300, 700, 200, 50, fill='lavender')
    drawLabel('Analyze', 400, 725, size=24, fill='white', font='verdana')
    drawProgressBar(app)

def handleCategoryMousePress(app, mouseX, mouseY):
    y = 100
    x = 50
    maxRowWidth = app.width - 50

    for category in app.categories:
        textWidth = getTextWidth(category, 20) + 40
        if x + textWidth > maxRowWidth:
            x = 50
            y += 70

        if x <= mouseX <= x + textWidth and y <= mouseY <= y + 50:
            if category in app.selectedCategories:
                app.selectedCategories.remove(category)
            else:
                app.selectedCategories.append(category)
        x += textWidth + 20

    if 300 <= mouseX <= 500 and 700 <= mouseY <= 750:  # Analyze button
        app.screen = 'analyze'
    handleProgressBarClick(app, mouseX, mouseY)

############################################################
# Analyze Screen
############################################################

def drawAnalyzeScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('Analyze Results', 20, 30, size=36, bold=True, fill='white', align='left', font='impact')
    drawLabel(f'Sound File URL: {app.soundURL}', app.width / 2, 200, size=20, fill='white', align='center', font='verdana')
    drawLabel('Selected Categories:', app.width / 2, 300, size=24, fill='white', align='center', font='verdana')
    y = 350
    for category in app.selectedCategories:
        drawLabel(f'- {category}', app.width / 2, y, size=20, fill='white', align='center', font='verdana')
        y += 40
    drawRoundedRect(300, 700, 200, 50, fill='lavender')
    drawLabel('Back to Start', 400, 725, size=24, fill='white', font='verdana')
    drawProgressBar(app)

def handleAnalyzeMousePress(app, mouseX, mouseY):
    if 300 <= mouseX <= 500 and 700 <= mouseY <= 750:  # Back to Start button
        app.screen = 'start'
        app.soundURL = ""
        app.selectedCategories = []
    handleProgressBarClick(app, mouseX, mouseY)

############################################################
# Shared Event Handlers
############################################################

def redrawAll(app):
    if app.screen == 'start':
        drawStartScreen(app)
    elif app.screen == 'categories':
        drawCategoryScreen(app)
    elif app.screen == 'analyze':
        drawAnalyzeScreen(app)

def onKeyPress(app, key):
    if app.screen == 'start':
        handleStartKeyPress(app, key)

def onMousePress(app, mouseX, mouseY):
    if app.screen == 'start':
        handleStartMousePress(app, mouseX, mouseY)
    elif app.screen == 'categories':
        handleCategoryMousePress(app, mouseX, mouseY)
    elif app.screen == 'analyze':
        handleAnalyzeMousePress(app, mouseX, mouseY)

############################################################
# Main
############################################################

def main():
    runApp(width=800, height=1000)

main()
