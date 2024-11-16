from cmu_graphics import *

def onAppStart(app):
    app.width = 800
    app.height = 1000
    app.screen = 'start'  # Initial screen
    app.soundURL = ""
    app.selectedCategories = []  # Tracks selected categories
    app.categories = [
        "Tempo", "Beats per Minute", "Duration", "Tone", "Key",
        "Dominant Timbres", "Rhythms", "Harmony", "Melody", "Pitch",
        "Volume", "Chords", "Structure", "Dynamics", "Mood",
        "Genre", "Instrumentation", "Phrasing", "Articulation", "Texture"
    ]
    app.categoryColors = ["lightpink", "lavender", "lightblue", "thistle", "plum", "powderblue"]
    app.categoryState = {category: False for category in app.categories}  # Tracks button states

############################################################
# Helper Functions for Rounded Buttons
############################################################

def drawRoundedRect(x, y, width, height, fill):
    cornerRadius = min(width, height) // 4
    drawRect(x + cornerRadius, y, width - 2 * cornerRadius, height, fill=fill)
    drawRect(x, y + cornerRadius, width, height - 2 * cornerRadius, fill=fill)
    drawCircle(x + cornerRadius, y + cornerRadius, cornerRadius, fill=fill)
    drawCircle(x + width - cornerRadius, y + cornerRadius, cornerRadius, fill=fill)
    drawCircle(x + cornerRadius, y + height - cornerRadius, cornerRadius, fill=fill)
    drawCircle(x + width - cornerRadius, y + height - cornerRadius, cornerRadius, fill=fill)

def getTextWidth(text, fontSize):
    return len(text) * fontSize * 0.6  # Estimate text width based on font size

############################################################
# Progress Bar and Navigation Helper
############################################################

def drawProgressBar(app):
    barY = app.height - 50
    dotRadius = 10
    gap = 60
    x1 = app.width / 2 - gap
    x2 = app.width / 2
    x3 = app.width / 2 + gap

    # Connecting lines
    if app.screen in ['categories', 'analyze']:
        drawLine(x1, barY, x2, barY, fill='white', lineWidth=2)
    if app.screen == 'analyze':
        drawLine(x2, barY, x3, barY, fill='white', lineWidth=2)

    # Dots
    drawCircle(x1, barY, dotRadius + (5 if app.screen in ['start', 'categories', 'analyze'] else 0), fill='white')
    drawCircle(x2, barY, dotRadius + (5 if app.screen in ['categories', 'analyze'] else 0), fill='white')
    drawCircle(x3, barY, dotRadius + (5 if app.screen == 'analyze' else 0), fill='white')

    # Arrows
    arrowSize = 20
    if app.screen != 'start':  # Left arrow
        drawLabel('<', 100, barY, size=arrowSize, fill='white', font='verdana')
    if app.screen != 'analyze':  # Right arrow
        drawLabel('>', app.width - 100, barY, size=arrowSize, fill='white', font='verdana')

def handleProgressBarClick(app, mouseX, mouseY):
    barY = app.height - 50
    # Left arrow click area
    if 80 <= mouseX <= 120 and barY - 20 <= mouseY <= barY + 20:
        if app.screen == 'categories':
            app.screen = 'start'
        elif app.screen == 'analyze':
            app.screen = 'categories'
    # Right arrow click area
    elif app.width - 120 <= mouseX <= app.width - 80 and barY - 20 <= mouseY <= barY + 20:
        if app.screen == 'start':
            app.screen = 'categories'
        elif app.screen == 'categories':
            app.screen = 'analyze'

############################################################
# Start Screen
############################################################

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Background
    # Main Title
    drawLabel('Audio Analyzer', 20, 20, size=36, bold=True, fill='white', font='impact', align='left')
    # Subtitle
    drawLabel('Input Sound URL', 20, 70, size=24, bold=False, fill='white', font='verdana', align='left')
    # Instructions
    drawLabel('Enter a sound file URL (http or cmu://):', app.width / 2, 200, size=20, fill='white', font='verdana', align='center')
    # Input URL
    drawLabel(app.soundURL, app.width / 2, 250, size=20, fill='white', font='verdana', align='center')

    # Next button
    drawRoundedRect(300, 400, 200, 50, fill='lavender')
    drawLabel('Next', 400, 425, size=24, fill='white', font='verdana')
    drawProgressBar(app)

def handleStartKeyPress(app, key):
    if key == "Enter":
        app.screen = 'categories'  # Proceed to categories screen
    elif key == "Backspace":
        app.soundURL = app.soundURL[:-1]
    else:
        app.soundURL += key

def handleStartMousePress(app, mouseX, mouseY):
    if 300 <= mouseX <= 500 and 400 <= mouseY <= 450:  # Next button
        app.screen = 'categories'

############################################################
# Category Selection Screen
############################################################

def drawCategoryScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Background
    # Main Title
    drawLabel('Audio Analyzer', 20, 20, size=36, bold=True, fill='white', font='impact', align='left')
    # Subtitle
    drawLabel('Select Categories', 20, 70, size=24, bold=False, fill='white', font='verdana', align='left')

    y = 100
    x = 50
    maxRowWidth = app.width - 50

    for i, category in enumerate(app.categories):
        textWidth = getTextWidth(category, 20) + 40  # Dynamic button size
        isSelected = app.categoryState[category]

        # Adjust row if button exceeds screen width
        if x + textWidth > maxRowWidth:
            x = 50
            y += 70

        # Highlight selected buttons
        buttonColor = 'yellow' if isSelected else app.categoryColors[i % len(app.categoryColors)]
        fontBold = True if isSelected else False

        drawRoundedRect(x, y, textWidth, 50, fill=buttonColor)
        drawLabel(category, x + textWidth / 2, y + 25, size=20, fill='black', font='verdana', bold=fontBold)
        x += textWidth + 20

    # Analyze button
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
            app.categoryState[category] = not app.categoryState[category]  # Toggle selection state
        x += textWidth + 20

    # Analyze button
    if 300 <= mouseX <= 500 and 700 <= mouseY <= 750:
        app.screen = 'analyze'

############################################################
# Analyze Screen
############################################################

def drawAnalyzeScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Background
    # Main Title
    drawLabel('Audio Analyzer', 20, 20, size=36, bold=True, fill='white', font='impact', align='left')
    # Subtitle
    drawLabel('Analyze Results', 20, 70, size=24, bold=False, fill='white', font='verdana', align='left')

    y = 200
    drawLabel(f'Sound File URL: {app.soundURL}', app.width / 2, 150, size=20, fill='white', font='verdana', align='center')
    drawLabel('Selected Categories:', app.width / 2, 180, size=20, fill='white', font='verdana', align='center')

    for category, selected in app.categoryState.items():
        if selected:
            drawLabel(f'- {category}', app.width / 2, y, size=20, fill='white', font='verdana', align='center')
            y += 30

    # Back to Start button
    drawRoundedRect(300, 700, 200, 50, fill='lavender')
    drawLabel('Back to Start', 400, 725, size=24, fill='white', font='verdana')
    drawProgressBar(app)

def handleAnalyzeMousePress(app, mouseX, mouseY):
    if 300 <= mouseX <= 500 and 700 <= mouseY <= 750:  # Back to Start button
        app.screen = 'start'
        app.soundURL = ""
        app.categoryState = {category: False for category in app.categories}  # Reset selections

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
    # Handle arrow clicks for navigation
    handleProgressBarClick(app, mouseX, mouseY)

############################################################
# Main
############################################################

def main():
    runApp(width=800, height=1000)

main()
