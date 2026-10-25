import flet as ft

from signin import signin_view
from signup import signup_view


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    def route_change(e=None):
        page.views.clear()
        page.views.append(signin_view(page))
        if page.route == "/signup":
            page.views.append(signup_view(page))
        page.update()

    async def view_pop(e):
        page.views.pop()
        await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)