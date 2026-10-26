import flet as ft

from signin import signin_view
from signup import signup_view
from supabase_client import supabase

PUBLIC_ROUTES = ["/", "/signup"]

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    def is_logged_in() -> bool:
        try:
            return supabase.auth.get_user() is not None
        except Exception:
            return False


    def route_change(e=None):
        route = page.route

        if route not in PUBLIC_ROUTES and not is_logged_in():
            route = "/"
        elif route in PUBLIC_ROUTES and is_logged_in():
            route = "/home"
        page.route = route

        page.views.clear()
        if page.route == "/home":
            # Temporary placeholder until home screen is implemented
            page.views.append(ft.View(route="/home", controls=[
                ft.Text("Signed in!"),
                ft.Button("Sign Out", on_click=sign_out),
            ]))
        else:
            page.views.append(signin_view(page))
            if page.route == "/signup":
                page.views.append(signup_view(page))
        page.update()

    async def sign_out(e):
        supabase.auth.sign_out()
        await page.push_route("/")

    async def view_pop(e):
        page.views.pop()
        await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)