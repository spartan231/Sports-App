# /// script
# dependencies = [
#   "pygame-ce",
#   "pygame_gui",
#   "python-i18n",
# ]
# ///
#

import pygame
import pygame_gui
import asyncio


def verifyuser(username, passwd):
  pass



async def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    titlefont = pygame.font.Font(None, 48)
    headingfont = pygame.font.Font(None, 32)
    smallfont = pygame.font.Font(None, 16)

    manager = pygame_gui.UIManager((640, 480))

    username_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(200, 165, 240, 35), manager=manager)
    password_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(200, 215, 240, 35), manager=manager)
    signinbtn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(225, 265, 200, 50), text="Sign In", manager=manager)
    signupbtn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(330, 350, 100, 25), text="Sign Up", manager=manager)

    while running:
        time_delta = clock.tick(60) / 1000.0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == signinbtn:
                    verifyuser(username_input.get_text(), password_input.get_text())

                if event.ui_element == signupbtn:
                    pass
            manager.process_events(event)



        manager.update(time_delta)
        screen.fill("lightblue")
        pygame.draw.rect(screen, "skyblue", (170, 140, 300, 200))
        title = titlefont.render("Sports App", True, "black")
        subheading = headingfont.render("Sign In", True, "black")
        signuptext = smallfont.render("No Account?", True, "black")

        screen.blit(title, (320 - (title.get_width()/2), 20))
        screen.blit(subheading, (320 - (subheading.get_width()/2), 115))
        screen.blit(signuptext, (320 - (subheading.get_width()/2) - 40, 360))


        manager.draw_ui(screen)
        pygame.display.flip()

        await asyncio.sleep(0)


asyncio.run(main())
