from rxconfig import config
from QuirkCraft.state import CraftState
import QuirkCraft.style as style
import reflex as rx

def topic_input() -> rx.Component:
    return rx.input(
        on_change=CraftState.set_topic,
        value=CraftState.topic,
        placeholder="Enter a topic like: Crypto, NFT, etc.",
        style=style.input_style,
        is_required=True
    )

def submit_button() -> rx.Component:
    return rx.button(
        "Generate",
        on_click=CraftState.helper,
        style=style.button_style
    )

def theme_selector() -> rx.Component:
    return rx.select(
        CraftState.options,
        on_change=CraftState.set_platform,
        value=CraftState.platform,
    )

def index() -> rx.Component:
    return rx.container(
        rx.hstack(
            rx.container(
                rx.container(
                    rx.heading(
                        "QuirkCraft",
                        style=style.heading_style
                    ),
                    rx.text(
                        "Craft captivating videos effortlessly with QuirkCraft. Whether you're a seasoned creator or just starting, empower your content creation journey today! 🚀✨",
                        style=style.quirkcraft_description
                    ),
                    style=style.top_container,
                ),
                rx.container(
                    rx.hstack(
                        rx.text(
                            "Platform: ",
                            style=style.text_style
                        ),
                        theme_selector(),
                        style={
                            "marginBottom": "15px",
                            "padding": "10px",
                            "fontSize": "16px",
                            "width": "80%",
                        }
                    ),
                    topic_input(),
                    submit_button(),
                    style=style.bottom_container,
                ),
                style=style.input_fragment
            ),
            rx.container(
                rx.container(
                    rx.text(
                        "Response:",
                        style=style.res_placeholder
                    ),
                    rx.text_area(
                        value=CraftState.TextualContent,
                        on_change=CraftState.set_TextualContent,
                        style=style.response_text_style,
                        is_read_only=True
                    ),
                    style=style.text_container
                ),
                rx.container(
                    rx.text(
                        "Image:",
                        style=style.img_placeholder
                    ),
                    rx.image(
                        src=CraftState.images[0],
                        style=style.image_style,
                        on_click=rx.download(url=CraftState.images[0])
                    ),
                    style=style.image_container
                ),
                style=style.output_container
            ),
            style=style.main_container
        ),
        style=style.index
    )


app = rx.App()
app.add_page(index)
app.compile()
