import engine

window = engine.window.Window()

while not window.exited:
    window.handle_events()
    window.update()

window.close()
