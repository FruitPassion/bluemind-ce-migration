from simple_term_menu import TerminalMenu


def create_terminal_menu(options, titre, multi_select=False, preselected_entries=[]):
    terminal_menu = TerminalMenu(options, title=titre, skip_empty_entries=True,
                                 multi_select=multi_select,
                                 show_multi_select_hint=multi_select,
                                 preselected_entries=preselected_entries
                                 )
    return terminal_menu, terminal_menu.show()
