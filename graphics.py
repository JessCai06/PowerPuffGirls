from cmu_graphics import *

def onAppStart(app):
    # Shared state
    app.width = 800
    app.height = 1000
    app.screen = 'start'  # Initial screen
    app.soundURL = ""
    app.selectedCategories = []
    app.categories = ["Category 1", "Category 2", "Category 3"]
    app.promptingSoundURL = True

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
        drawLabel('<', 100, barY, size=arrowSize, fill='white')
    if app.screen != 'analyze':  # Show right arrow
        drawLabel('>', app.width - 100, barY, size=arrowSize, fill='white')

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
    drawLabel('Input Sound URL', 20, 30, size=36, bold=True, fill='white', align='left')
    drawLabel('Enter a sound file URL (http or cmu://):', app.width / 2, 200, size=24, fill='white', align='center')
    drawLabel(app.soundURL, app.width / 2, 250, size=20, fill='white', align='center')
    drawRect(300, 400, 200, 50, fill='gray', border='white')
    drawLabel('Next', 400, 425, size=24, fill='white')
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
    drawLabel('Select Categories', 20, 30, size=36, bold=True, fill='white', align='left')
    y = 200
    for i, category in enumerate(app.categories):
        isSelected = category in app.selectedCategories
        drawRect(300, y, 200, 50, fill='green' if isSelected else 'gray', border='white')
        drawLabel(category, 400, y + 25, size=20, fill='white' if isSelected else 'black')
        y += 80
    drawRect(300, 700, 200, 50, fill='gray', border='white')
    drawLabel('Analyze', 400, 725, size=24, fill='white')
    drawProgressBar(app)

def handleCategoryMousePress(app, mouseX, mouseY):
    y = 200
    for i, category in enumerate(app.categories):
        if 300 <= mouseX <= 500 and y <= mouseY <= y + 50:
            if category in app.selectedCategories:
                app.selectedCategories.remove(category)
            else:
                app.selectedCategories.append(category)
        y += 80
    if 300 <= mouseX <= 500 and 700 <= mouseY <= 750:  # Analyze button
        app.screen = 'analyze'
    handleProgressBarClick(app, mouseX, mouseY)

############################################################
# Analyze Screen
############################################################

def drawAnalyzeScreen(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Darker background
    drawLabel('Analyze Results', 20, 30, size=36, bold=True, fill='white', align='left')
    drawLabel(f'Sound File URL: {app.soundURL}', app.width / 2, 200, size=20, fill='white', align='center')
    drawLabel('Selected Categories:', app.width / 2, 300, size=24, fill='white', align='center')
    y = 350
    for category in app.selectedCategories:
        drawLabel(f'- {category}', app.width / 2, y, size=20, fill='white', align='center')
        y += 40
    drawRect(300, 700, 200, 50, fill='gray', border='white')
    drawLabel('Back to Start', 400, 725, size=24, fill='white')
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
