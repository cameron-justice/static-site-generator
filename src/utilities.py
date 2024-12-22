def format_markdown_image(alt: str, link: str) -> str:
    """
        Create markdown image string from alt text and link
    """
    return f"![{alt}]({link})"

def format_markdown_link(text: str, link: str) -> str:
    """
        Create markdown link string from text and link
    """
    return f"[{text}]({link})"