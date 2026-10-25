import flet as ft

def signup_view(page: ft.Page) -> ft.View:
    email = ft.TextField(label="Email", width=400)
    password = ft.TextField(label="Password", width=400, password=True, can_reveal_password=True)

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
                        email,
                        password,
                        ft.Button("Sign Up", width=400, on_click=lambda e: print(email.value, password.value)),
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