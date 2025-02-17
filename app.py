import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text, Alert, ButtonAlert, Modal, FieldArray, Select, FieldMatriz
from flet import RouteChangeEvent, ViewPopEvent
from classApp.Methods.Binaria import BinariaEstaciones
from classApp.Methods.EnteraMixta import EnteraMixta
from classApp.Methods.EnteraPura import EnteraPura
from classApp.Methods.Mochila import Mochila
from classApp.Methods.RamificacionAcotacion import RamificacionAcotacion 
from classApp.Methods.createTxt import createTXT
from classApp.Methods.PlanosCortes import PlanosCortes
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
BINARIA = BinariaEstaciones()
ENTERA = EnteraMixta()
RAMIFICACION = RamificacionAcotacion()
PURA = EnteraPura()
MOCHILA = Mochila()
PLANOS = PlanosCortes()


def main(page: ft.Page) -> None:
    page.title = "Calculadora Programacion Entera"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    page.window.center()
    page.window.resizable = False

    alert = Alert([ButtonAlert("Close", lambda _: page.close(alert))])
    modal = Modal()

    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    ft.Column([Text("Bienvenido a calculadora Entera", 20, "w150"), Text("Menú", 40, "w800")], 
                    spacing=0, horizontal_alignment=ALIGN_HOR),
                    ft.Row([ Button("Binaria", lambda _: page.go('/binaria')), Button("Entera Mixta", lambda _: page.go('/mixta')), Button("Ramificacion Acotacion", lambda _: page.go('/ramificacion'))], 
                    spacing=10, alignment=ALIGN_VERT),
                    ft.Row([ Button("Entera Pura", lambda _: page.go('/pura')), Button("Mochila", lambda _: page.go('/mochila')), Button("Planos de Corte", lambda _: page.go('/planos'))], 
                    spacing=10, alignment=ALIGN_VERT)
                ])
        )

# Binaria
        if page.route == '/binaria':
            field_1 = Field("Número de ciudades", value=10)
            field_2 = FieldMatriz("Distancias", width=800, value="0,35,20,40,30,60,60,20,55,32;35,0,45,35,20,70,30,45,45,34;20,45,0,15,55,20,80,0,90,56;40,35,15,0,65,35,12,15,24,60;30,20,55,65,0,40,40,20,15,12;60,70,20,35,40,0,15,32,0,12;30,40,32,12,55,25,0,34,65,55;80,12,34,67,45,60,65,0,30,45;12,34,56,78,90,100,35,20,0,90;40,12,40,20,24,10,12,0,20,0")
            field_3 = Field("Tiempo máximo", value=40)
            def _(e) -> None:
                try:
                    BINARIA.set_parameters(int(field_1.getValue()), field_2.getValues(), int(field_3.getValue()))
                    BINARIA.pre_solve()
                    BINARIA.solve()
                    BINARIA.result()
                    modal.openModal(page, "Resultado", [ft.Text(BINARIA.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(BINARIA.getResult(), "Binaria")
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
                    ft.Row([field_1, field_3], alignment=ALIGN_VERT, spacing=5), 
                    ft.Row([field_2], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
                ])
            )


        # Entero Mixto
        if page.route == '/mixta':
            field_1 = Field("Valor de X en función objetivo", value=4)
            field_2 = Field("Valor de Y en función objetivo", value=3)
            field_3 = Field("Valor de x en restricción", width=150, value=3)
            field_4 = Field("Valor de y en restricción", width=150, value=2)
            field_5 = Field("Restriccion 1", width=150, value=18)
            select = Select("Tipo", ["max", "min"])
            select.value = "max"
            def _(e) -> None:
                try:
                    ENTERA.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), str(select.getValue()))
                    ENTERA.solve()
                    ENTERA.result()
                    modal.openModal(page, "Resultado", [ft.Text(ENTERA.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(ENTERA.getResult(), "Entera Mixta")
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('/mixta',
                [
                    Text('Entera Mixta', 35, "w800"),
                    ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5), 
                    ft.Row([field_3, field_4, field_5], alignment=ALIGN_VERT, spacing=3),
                    ft.Row([select], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
                ])
            )

        # Ramificacion Acotacion
        if page.route == '/ramificacion':
            field_1 = Field("Valor de X", value=3)
            field_2 = Field("Valor de Y", value=2)
            field_3 = Field("Restriccion 1", width=150, value=4)
            field_4 = Field("Restriccion 2", width=150, value=0)
            field_5 = Field("Valor X de Restriccion 1", width=150, value=4)
            field_6 = Field("Valor X de Restriccion 2", width=150, value=1)
            field_7 = Field("Valor Y de Restriccion 1", width=150, value=4)
            field_8 = Field("Valor Y de Restriccion 2", width=150, value=1)
            select = Select("Tipo", ["max", "min"])
            select.value = "max"
            def _(e) -> None:
                try:
                    RAMIFICACION.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), str(select.getValue()), int(field_5.getValue()),int(field_6.getValue()), int(field_7.getValue()), int(field_8.getValue()))
                    RAMIFICACION.solve()
                    RAMIFICACION.result()
                    modal.openModal(page, "Resultado", [ft.Text(RAMIFICACION.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(RAMIFICACION.getResult(), "Ramificacion Acotacion")
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('/ramificacion',
                [
                    Text('Ramificacion Acotacion', 35, "w800"),
                    ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=3),
                    ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=3),
                    ft.Row([field_7, field_8], alignment=ALIGN_VERT, spacing=3),
                    ft.Row([select], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
                ])
            )
        
        # Entero Pura
        if page.route == '/pura':
            field_1 = Field("Valor de X", value=5)
            field_2 = Field("Valor de Y", value=3)
            field_3 = Field("Coe. 1 Restriccion 1", width=90, value=2)
            field_4 = Field("Coe. 2 Restriccion 1", width=90, value=3)
            field_5 = Field("Coe. 1 Restriccion 2", width=90, value=2)
            field_6 = Field("Coe. 2 Restriccion 2", width=90, value=1)
            field_7 = Field("Restriccion 1 menor que", value=12)
            field_8 = Field("Restriccion 2 menor que", value=8)
            select = Select("Tipo", ["max", "min"])
            select.value = "max"
            def _(e) -> None:
                try:
                    PURA.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_7.getValue()), int(field_5.getValue()), int(field_6.getValue()), int(field_8.getValue()) ,str(select.getValue()))
                    PURA.solve()
                    PURA.result()
                    modal.openModal(page, "Resultado", [ft.Text(PURA.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(PURA.getResult(), "Entera Pura")
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('/pura',
                [
                    Text('Entera Pura', 35, "w800"),
                    ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5), 
                    ft.Row([field_3, field_4, field_5, field_6], alignment=ALIGN_VERT, spacing=2),
                    ft.Row([field_7, field_8], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([select], alignment=ALIGN_VERT, spacing=5),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
                ])
            )
        # Mochilla
        if page.route == '/mochila':
            field_1 = FieldArray("Valores", value="3, 6, 5, 5, 7")
            field_2 = FieldArray("Pesos", value="15, 25, 12, 10, 15")
            field_3 = Field("Capacidad", width=150, value=120)
            select = Select("Tipo", ["max", "min"])
            select.value = "max"
            def _(e) -> None:
                try:
                    MOCHILA.set_atr(field_1.getValues(), field_2.getValues(), int(field_3.getValue()), str(select.getValue()))
                    MOCHILA.resolver()
                    MOCHILA.mostrar_resultados()
                    modal.openModal(page, "Resultado", [ft.Text(MOCHILA.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(MOCHILA.getResult(), "Mochila")
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('/mochila',
                [
                    Text('Mochila', 35, "w800"),
                    ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5), 
                    ft.Row([field_3, select], alignment=ALIGN_VERT, spacing=3),
                    ft.Row([
                        Button('Calcular', click_action=_),
                        Button('Volver a menú', lambda _: page.go('/'))
                    ], alignment=ALIGN_VERT, spacing=5)
                     ])
                )
            
        # Planos y Cortes
        if page.route == '/planos':
            field_1 = FieldArray("Coeficientes de la función objetivo", value="5, 4")
            field_2 = FieldMatriz("Coeficientes de las restricciones", width=300, value="6, 4, 1, 2, -1, 1")
            field_3 = FieldArray("Valores de las restricciones", value="24, 6, 1")
            def _(e) -> None:
                try:
                    PLANOS.set_atr(field_1.getValues(), field_2.getValues(), field_3.getValues())
                    PLANOS.solve()
                    PLANOS.result()
                    modal.openModal(page, "Resultado", [ft.Text(PLANOS.getResult(), color=COLOR_SECOND), Button("Cerrar", lambda _: page.close(modal))])
                    createTXT(PlanosCortes.getResult(), "Planos y Cortes")
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    print(traceback.format_exc())
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('/planos',
                [
                    Text('Planos y Cortes', 35, "w800"),
                    ft.Row([field_1], alignment=ALIGN_VERT), 
                    ft.Row([field_2], alignment=ALIGN_VERT), 
                    ft.Row([field_3], alignment=ALIGN_VERT), 
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