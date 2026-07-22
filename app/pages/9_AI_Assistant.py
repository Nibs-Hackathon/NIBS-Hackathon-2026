"""Legacy deep-link for Command Nexus.

NEX is now the global assistant entry point. This route remains available for
bookmarked URLs without duplicating the chat interface or backend calls.
"""

from ui_helpers import page_heading, render_sidebar, setup_page


setup_page("AI Assistant")
render_sidebar("Command Nexus")
page_heading(
    "COMMAND NEXUS",
    "NEX is ready",
    "Use the floating NEX companion in the lower-left corner to open your operations copilot.",
)
