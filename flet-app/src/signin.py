import flet as ft
from supabase import AuthApiError

from supabase_client import supabase


def signin_view(page: ft.Page) -> ft.View:
    email = ft.TextField(label="Email", width=400)
    password = ft.TextField(label="Password", width=400, password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED_400)

    async def sign_in(e):
        try:
            supabase.auth.sign_in_with_password({"email": email.value, "password": password.value})
        except AuthApiError as err:
            error.value = err.message
            error.update()
            return
        await page.push_route("/home")

    async def go_to_signup(e):
        await page.push_route("/signup")

    return ft.View(
        route="/",
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Sports App", size=50),
            ft.Container(content=ft.Text("Sign In", size=35), padding=ft.Padding.only(top=30)),
            ft.Container(
                width=500,
                bgcolor=ft.Colors.GREY_900,
                border_radius=ft.BorderRadius.all(12),
                padding=20,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        email,
                        password,
                        ft.Button("Sign In", width=400,
                                  on_click=sign_in),
                        error,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("Don't have an account?"),
                                ft.TextButton("Sign Up", on_click=go_to_signup),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )