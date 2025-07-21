import reflex as rx

@rx.page(route="/teste")
def teste_page():
    return rx.heading("Ola, Mundo! A rota funciona.", size="9")