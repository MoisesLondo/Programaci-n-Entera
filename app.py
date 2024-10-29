import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text, Alert, ButtonAlert, Modal
from flet import RouteChangeEvent, ViewPopEvent
from classApp.Methods.Binaria import Binaria
from classApp.Methods.EnteraMixta import EnteraMixta
from classApp.Methods.EnteraPura import EnteraPura
from classApp.Methods.Mochila import Mochila
from classApp.Methods.RamificacionAcotacion import RamificacionAcotacion 
from classApp.Methods.createTxt import createTXT
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

# ASIGNACION de Clases
BINARIA = Binaria()


def main(page: ft.Page) -> None:
    page.title = "Calculadora Programacion Entera"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    page.window.center()
    page.window.resizable = False

    alert = Alert([ButtonAlert("Close", lambda _: page.close(alert))])

    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    ft.Column([Text("Bienvenido a calculadora Entera", 20, "w150"), Text("Menú", 40, "w800")], 
                    spacing=0, horizontal_alignment=ALIGN_HOR),
                    ft.Row([ Button("Binaria", lambda _: page.go('/binaria'))], 
                    spacing=10, alignment=ALIGN_VERT),
                    ft.Row([], 
                    spacing=10, alignment=ALIGN_VERT)
                ])
        )

        # Binaria
        if page.route == '/binaria':
            field_1 = Field("Valor 1",width=150)
            field_2 = Field("Valor 2",width=150)
            field_3 = Field("Valor 3",width=150)
            field_4 = Field("Res 1")
            field_5 = Field("Res 2")
            field_6 = Field("Type", value="max")
            def _(e) -> None:
                try:
                    BINARIA.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), str(field_6.getValue()))
                    BINARIA.result()
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
            ViewClass('/binaria', 
                [
                    Text('Binaria', 35, "w800"),
                    ft.Row([field_1, field_2, field_3], alignment=ALIGN_VERT, spacing=3), 
                    ft.Row([field_4, field_5], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([field_6], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
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