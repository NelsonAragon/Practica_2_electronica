"""
Editor de Sprites (8-bits) con Flet
Electrónica Digital - Ingeniería de Sistemas - CUL

Implementa las 4 fases de la guía:
  Fase 1: Matriz 8x8 con GridView (framebuffer)
  Fase 2: Panel de control (TextField, botón, texto dinámico) + eventos de clic
  Fase 3: Pantalla -> Hexadecimal (barrido de la matriz, binario de 64 bits -> hex)
  Fase 4: Hexadecimal -> Pantalla (validación, expansión binaria, renderizado)
"""

import flet as ft

ROWS, COLS = 8, 8
OFF_COLOR = "#1e2130"      # píxel apagado
ON_COLOR = "#39ff14"       # píxel encendido (verde neón)


def main(page: ft.Page):
    # ---------- Fase 1: Ventana principal ----------
    page.title = "Editor de Sprites 8x8 - Flet"
    page.window_width = 520
    page.window_height = 720
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d0f1a"
    page.padding = 24
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Framebuffer: matriz 8x8 de Containers (creada con bucle anidado)
    pixels = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def toggle_pixel(e):
        btn = e.control
        btn.bgcolor = ON_COLOR if btn.bgcolor == OFF_COLOR else OFF_COLOR
        refresh_hex_output()

    grid_controls = []
    for r in range(ROWS):
        for c in range(COLS):
            btn = ft.Container(
                width=40,
                height=40,
                bgcolor=OFF_COLOR,
                border_radius=6,
                border=ft.border.all(1, "#2c3050"),
                on_click=toggle_pixel,
                animate=100,
            )
            pixels[r][c] = btn
            grid_controls.append(btn)

    grid = ft.GridView(
        controls=grid_controls,
        runs_count=COLS,
        spacing=4,
        run_spacing=4,
        width=COLS * 44,
        height=ROWS * 44,
    )

    # ---------- Fase 2: Panel de control ----------
    hex_display = ft.Text(
        "0000000000000000",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ON_COLOR,
        font_family="Consolas, monospace",
    )

    hex_input = ft.TextField(
        label="Código Hex (máx. 16 caracteres)",
        width=280,
        max_length=16,
        capitalize=ft.TextCapitalization.CHARACTERS,
        border_color="#2c3050",
    )

    # ---------- Fase 3: Pantalla -> Hexadecimal ----------
    def refresh_hex_output():
        # Barrido secuencial de los 64 elementos -> cadena binaria de 64 bits
        binary = "".join(
            "1" if pixels[r][c].bgcolor == ON_COLOR else "0"
            for r in range(ROWS)
            for c in range(COLS)
        )
        value = int(binary, 2)
        # Salida en mayúsculas, longitud fija de 16 caracteres, rellenada con ceros
        hex_display.value = format(value, "016X")
        page.update()

    # ---------- Fase 4: Hexadecimal -> Pantalla ----------
    def load_hex(e):
        text = (hex_input.value or "").strip().upper()

        # Validación: máximo 16 caracteres y solo dígitos hexadecimales (0-9, A-F)
        valid_chars = set("0123456789ABCDEF")
        if not text or len(text) > 16 or not all(ch in valid_chars for ch in text):
            hex_input.error_text = "Ingresa de 1 a 16 caracteres hexadecimales válidos (0-9, A-F)"
            page.update()
            return

        hex_input.error_text = None

        # Expansión binaria: exactamente 64 caracteres, rellenando con ceros a la izquierda
        value = int(text, 16)
        binary = format(value, "064b")

        # Renderizado visual: recorre los 64 bits en paralelo con los 64 botones
        idx = 0
        for r in range(ROWS):
            for c in range(COLS):
                pixels[r][c].bgcolor = ON_COLOR if binary[idx] == "1" else OFF_COLOR
                idx += 1

        refresh_hex_output()

    load_button = ft.FilledButton("Cargar Hex", icon=ft.icons.UPLOAD, on_click=load_hex)

    def clear_grid(e):
        for r in range(ROWS):
            for c in range(COLS):
                pixels[r][c].bgcolor = OFF_COLOR
        refresh_hex_output()

    clear_button = ft.OutlinedButton("Limpiar", icon=ft.icons.CLEAR, on_click=clear_grid)

    # ---------- Layout ----------
    page.add(
        ft.Text("Editor de Sprites 8×8", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("Electrónica Digital · Ingeniería de Sistemas · CUL", size=12, color="#8a8fb0"),
        ft.Divider(color="#2c3050"),
        ft.Row([hex_input, load_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [ft.Text("Valor Hexadecimal actual:", size=14, color="#8a8fb0"), hex_display],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        ft.Container(content=grid, alignment=ft.alignment.center, padding=10),
        ft.Row([clear_button], alignment=ft.MainAxisAlignment.CENTER),
    )

    refresh_hex_output()


if __name__ == "__main__":
    ft.app(target=main)
