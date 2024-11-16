from cmu_graphics import *

def onAppStart(app):
    # List of available fonts
    app.fonts = [
        'monospace', 'serif', 'sansSerif', 'cursive', 'fantasy',
        'helvetica', 'arial', 'verdana', 'timesNewRoman', 'georgia',
        'comicSansMS', 'courierNew', 'impact', 'trebuchetMS', 'lucidaConsole',
        'lucidaSans', 'garamond', 'palatino', 'tahoma', 'arialBlack'
    ]
    app.startY = 50
    app.lineSpacing = 40

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='black')  # Dark background
    drawLabel("Available Fonts in CMU Graphics", app.width / 2, 30, size=24, fill='white', bold=True)
    
    y = app.startY
    for font in app.fonts:
        drawLabel(font, 400, y, size=20, font=font, fill='white', align='center')
        y += app.lineSpacing

def main():
    runApp(width=800, height=1000)

main()
