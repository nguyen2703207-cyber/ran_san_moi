        logo = pygame.transform.scale(logo, (cell_size*cell_number, cell_size*cell_number))
        logo_rect = logo.get_rect(topleft=(0,0))
        screen.blit(logo, logo_rect)