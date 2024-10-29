import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text, Alert, ButtonAlert, Modal
from flet import RouteChangeEvent, ViewPopEvent
from classApp.methods.Binaria import Binaria
from classApp.methods.EnteraMixta import EnteraMixta
from classApp.methods.EnteraPura import EnteraPura
from classApp.methods.Mochila import Mochila
from classApp.methods.RamificacionAcotacion import RamificacionAcotacion 
# Import the new class
import yaml
import traceback

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
WIDTH = config['size']['width']
HEIGHT = config['size']['height']
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']

def main(page: ft.Page) -> None:
    page.title = "Calculadora Simulaciones"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    page.window.center()
    page.window.resizable = False

    alert = Alert([ButtonAlert("Close", lambda _: page.close(alert))])

    def createTXT(content, title = None):
        with open('output.txt', 'a') as f:
            if title:
                f.write(f'\n------------------------------------------{title}------------------------------------------')
            if isinstance(content, list):
                f.write('\n')
                for item in content:
                    f.write(f'{item}\n')
            else:
                f.write('\n')
                f.write(content)
        

    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    ft.Column([Text("Bienvenido a calculadora simulaciones", 20, "w150"), Text("Menú", 40, "w800")], 
                    spacing=0, horizontal_alignment=ALIGN_HOR),
                    ft.Row([], 
                    spacing=10, alignment=ALIGN_VERT),
                    ft.Row([], 
                    spacing=10, alignment=ALIGN_VERT)
                ])
        )

        page.update()
    
    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = router_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()

if __name__ == "__main__":
    ft.app(main)