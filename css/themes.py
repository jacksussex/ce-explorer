import solara
import css.colour_scheme_classes as colours

def apply_theme():
    solara.lab.theme.dark = False
    solara.lab.theme.themes.light.primary = colours.SECONDARY
    solara.lab.theme.themes.light.secondary = colours.PRIMARY
    solara.lab.theme.themes.light.accent = colours.ACCENT
    solara.lab.theme.themes.light.error = colours.ERROR
    solara.lab.theme.themes.light.info = colours.INFO