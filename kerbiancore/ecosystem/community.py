def community_plugin_template(name, description, author, main_func):
    """
    Returns a standard plugin dict for sharing.
    """
    return {
        "name": name,
        "description": description,
        "author": author,
        "entrypoint": main_func,
        "version": "1.0.0"
    }

def example_community_greet_plugin():
    def greet(name="world"):
        print(f"Hello, {name}! Shared from KerbianCore Community.")
    return community_plugin_template(
        name="community_greet",
        description="Say hello from the community.",
        author="open-source-user",
        main_func=greet
    )