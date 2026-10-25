import flet as ft
from supabase import AuthApiError

from supabase_client import supabase


def signup_view(page: ft.Page) -> ft.View:
    username = ft.TextField(label="Username", width=400)
    email = ft.TextField(label="Email", width=400)
    password = ft.TextField(label="Password", width=400, password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED_400)

    async def sign_up(e):
        try:
            supabase.auth.sign_up({
                "email": email.value,
                "password": password.value,
                "options": {"data": {"username": username.value}},
            })
        except AuthApiError as err:
            # The trigger's insert fails if the username is taken or not 3-24 chars
            if "Database error" in err.message:
                error.value = "Username must be 3-24 characters and not already taken"
            else:
                error.value = err.message
            error.update()
            return
        await page.push_route("/home")

    async def go_to_signin(e):
        await page.push_route("/")

    return ft.View(
        route="/signup",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Sports App", size=50),
            ft.Container(content=ft.Text("Sign Up", size=35), padding=ft.Padding.only(top=30)),
            ft.Container(
                width=500,
                bgcolor=ft.Colors.GREY_900,
                border_radius=ft.BorderRadius.all(12),
                padding=20,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        username,
                        email,
                        password,
                        ft.Button("Sign Up", width=400, on_click=sign_up),
                        error,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Already have an account?"),
                                ft.TextButton("Sign In", on_click=go_to_signin),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )