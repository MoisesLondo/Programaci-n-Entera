import yaml
import flet as ft
from typing import List, Any


#Lectura del archivo config
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
    # ALINIAMIENTO
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
    # COLORES DE LA APP
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']
DANGER = config['colors']['danger']
    # OTROS
STATE = ft.ControlState

#CLASE BOTON
class Button(ft.ElevatedButton):
    def __init__(self, text: str, click_action):
        super().__init__()
        self.text= text
        self.bgcolor= COLOR_SECOND
        self.color= COLOR_PRIMARY
        self.on_click = click_action
        self.style = ft.ButtonStyle(
            color={
                STATE.HOVERED: COLOR_SECOND,
                STATE.FOCUSED: COLOR_PRIMARY,
                STATE.DEFAULT: COLOR_PRIMARY
            },
            bgcolor={
                STATE.HOVERED: COLOR_PRIMARY,
                STATE.DEFAULT: COLOR_SECOND,
            },
            side={
                STATE.HOVERED: ft.BorderSide(2, COLOR_SECOND),
            }
        )
#CLASE View
class ViewClass(ft.View):
    def __init__(self, router: str, controls):
        super().__init__()
        self.route = router
        self.controls = controls
        self.bgcolor = COLOR_PRIMARY
        self.vertical_alignment = ALIGN_VERT
        self.horizontal_alignment = ALIGN_HOR

#CLASE TextField
class Field(ft.Container):
    def __init__(self, label: str, width: int=200, value=0) -> None:
        super().__init__()
        self._TextField = ft.TextField(
            bgcolor=COLOR_PRIMARY, 
            cursor_color=COLOR_SECOND, 
            color=COLOR_SECOND, 
            border_color=COLOR_SECOND,
            text_align= ALIGN_VERT,
            text_size=config['input']['text-size'],
            height=config['input']['height'],
            value=value,
            width = width
        )
        self.content=ft.Column([
            ft.Text(value=label, color=COLOR_SECOND),
            self._TextField
        ], spacing=5)
        self.padding=10
    
    def getValue(self):
        return self._TextField.value

class Text(ft.Text):
    def __init__(self, value: str, size: int, weight: str):
        super().__init__()
        self.value = value
        self.size = size
        self.color = COLOR_SECOND
        self.bgcolor = COLOR_PRIMARY
        self.weight = weight

class Modal(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.bgcolor = COLOR_PRIMARY
    
    def openModal(self, page:ft.Page, title:str, content:[]) -> None:
        self.title = ft.Text(title, color=COLOR_SECOND)
        self.content = ft.Column(controls=content, spacing=5, scroll=ft.ScrollMode.AUTO)
        page.open(self)

class Alert(ft.AlertDialog):
    def __init__(self, actions) -> None:
        super().__init__()
        self.modal = True
        self.bgcolor = DANGER
        self.title=ft.Text('Mensaje de Error', color=COLOR_PRIMARY)
        self.actions= actions
    
    def openAlert(self, page: ft.Page, text) -> None:
        self.content= ft.Text(text, color=COLOR_PRIMARY)
        page.open(self)


class ButtonAlert(ft.ElevatedButton):
    def __init__(self, text: str, click_action) -> None:
        super().__init__()
        self.text = text
        self.bgcolor = COLOR_PRIMARY
        self.color = DANGER
        self.on_click = click_action
        self.style = ft.ButtonStyle(
            color={
                STATE.HOVERED: DANGER,
                STATE.FOCUSED: DANGER,
                STATE.DEFAULT: COLOR_PRIMARY
            },
            bgcolor={
                STATE.HOVERED: COLOR_PRIMARY,
                STATE.DEFAULT: DANGER,
            },
            side={
                STATE.DEFAULT: ft.BorderSide(2,COLOR_PRIMARY),
            }
        )

class FieldArray(Field):
    def __init__(self, label: str, width: int=200, value=0) -> None:
        Field.__init__(self, label, width, value) 
        self.content=ft.Column([
            ft.Text(value=label, color=COLOR_SECOND),
            self._TextField,
            ft.Text(value="Separar los valores con ,", color=COLOR_SECOND)
        ], spacing=5)
        
    def getValues(self) -> []:
        self.values = []
        for number in self.getValue().split(','):
            self.values.append(int(number))
        print(f"{self.values}")
        return self.values

class FieldMatriz(Field):
    def __init__(self, label: str, width: int=200, value="") -> None:
        super().__init__(label, width, value)
        self.content = ft.Column([
            ft.Text(value=label, color=COLOR_SECOND),
            self._TextField,
            ft.Text(value="Ingrese filas separadas por ';' y valores por ','", color=COLOR_SECOND, size=12)
        ], spacing=5)

    def getValues(self) -> []:
        matrix = []
        rows = self.getValue().split(';')
        for row in rows:
            matrix.append([int(val.strip()) for val in row.split(',')])
        print(f"Matrix: {matrix}")
        return matrix

class Select(ft.Dropdown):
    def __init__(self, label: str, values: List[str], width: int = 200) -> None:
        super().__init__()
        self.label = label
        self.values = values
        self.width = width
        self.bgcolor = COLOR_PRIMARY
        self.color = COLOR_SECOND
        self.border_color = COLOR_SECOND
        self.cursor_color = COLOR_SECOND
        self.text_align = ALIGN_VERT
        self.text_size = config['input']['text-size']
        self.height = config['input']['height']
        self.value = values[0] if values else None
        self.options = [ft.dropdown.Option(v) for v in values]

    def getValue(self):
        return self.value