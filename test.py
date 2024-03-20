import curses

def draw_menu(stdscr):
    # Configuración inicial
    curses.curs_set(0)  # Ocultar el cursor
    stdscr.nodelay(1)   # Establecer modo sin bloqueo para la entrada

    # Inicializar variables
    current_option = 0
    options = ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5", "Opción 6", "Opción 7", "Opción 8", "Opción 9", "Salir"]

    # Obtener dimensiones de la pantalla
    height, width = stdscr.getmaxyx()

    # Dibujar el banner
    banner = "Bienvenido al Menú"
    banner_x = (width - len(banner)) // 2
    stdscr.addstr(0, banner_x, banner)

    # Calcular la cantidad de filas necesarias para las opciones
    num_rows = len(options) // 3 + 1

    # Ciclo principal
    while True:

        # Dibujar las opciones
        for i, option in enumerate(options):
            row = (height - num_rows) // 2 + i // 3  # Calcular la fila correspondiente
            col = (width // 3) * (i % 3)             # Calcular la columna correspondiente

            if i == current_option:
                stdscr.addstr(row, col, option, curses.A_REVERSE)
            else:
                stdscr.addstr(row, col, option)

        # Obtener la entrada del teclado
        key = stdscr.getch()

        # Procesar la entrada del teclado
        if key == curses.KEY_UP:
            current_option = (current_option - 3) % len(options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 3) % len(options)
        elif key == curses.KEY_LEFT:
            current_option = (current_option - 1) % len(options)
        elif key == curses.KEY_RIGHT:
            current_option = (current_option + 1) % len(options)
        elif key == 10:  # Tecla Enter
            if current_option == len(options) - 1:
                break  # Salir del bucle si se selecciona "Salir"

        # Actualizar la pantalla
        stdscr.refresh()

# Inicializar curses y ejecutar el programa
curses.wrapper(draw_menu)
