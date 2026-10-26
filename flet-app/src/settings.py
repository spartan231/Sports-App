import flet as ft


def settings_view(page: ft.Page) -> ft.View:
    # State: mock followed teams replace with for loop that goes through users followed teams list
    followed_teams = [
        {"id": "1", "name": "Miami Dolphins", "league": "NFL"},
        {"id": "2", "name": "Pittsburgh Steelers", "league": "NFL"},
        {"id": "3", "name": "Tampa Bay Buccaneers", "league": "NFL"},
        {"id": "4", "name": "Jacksonville Jaguars", "league": "NFl"},
    ]
    #n=0
    #for team in user.followed_teams:
    #   followed_teams.append(n, team, "NFL")

    new_team_input = ft.TextField(
        hint_text="Add team name...",
        expand=True,
        dense=True,
    )

    teams_list_column = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)

    def remove_team(team_id: str):
        nonlocal followed_teams
        followed_teams = [t for t in followed_teams if t["id"] != team_id]
        # user.remove_team(team)
        render_teams()

    def add_team(e):
        #leaving this in but i dont know if we will be adding teams in settings
        val = new_team_input.value.strip()
        if not val:
            return
        # user.add_team(team)
        followed_teams.append({
            "id": str(len(followed_teams) + 1),
            "name": val,
            "league": "Custom",
        })
        new_team_input.value = ""
        render_teams()

    def build_team_row(team: dict) -> ft.Container:
        return ft.Container(
            bgcolor=ft.Colors.GREY_900,
            border_radius=8,
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(ft.Icons.SPORTS_FOOTBALL, color=ft.Colors.AMBER_400),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(team["name"], size=16, weight=ft.FontWeight.W_600),
                                    ft.Text(team["league"], size=12, color=ft.Colors.GREY_400),
                                ],
                            ),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_400,
                        tooltip="Unfollow team",
                        on_click=lambda e, tid=team["id"]: remove_team(tid),
                    ),
                ],
            ),
        )

    def render_teams():
        teams_list_column.controls.clear()
        if not followed_teams:
            teams_list_column.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=30,
                    content=ft.Text("No followed teams yet.", color=ft.Colors.GREY_500, size=15),
                )
            )
        else:
            for team in followed_teams:
                teams_list_column.controls.append(build_team_row(team))
        page.update()

    # Layout assembly
    page.add(
        ft.AppBar(
            title=ft.Text("Settings - Followed Teams"),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        ),
        ft.Container(
            width=600,
            padding=20,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text("Manage Followed Teams", size=22, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            new_team_input,
                            ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=add_team),
                        ]
                    ),
                    ft.Divider(color=ft.Colors.GREY_800),
                    teams_list_column,
                ],
            ),
        ),
    )
    render_teams()

    if __name__ == "__main__":
        ft.app(target=settings_view)