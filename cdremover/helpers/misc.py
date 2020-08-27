def get_foreground(config:dict):
    """Function to get the foreground color for the current theme"""
    if config["mode"] == "light":
        return "#5c616c"
    elif config["mode"] == "dark":
        return "#a6a6a6"
    else:
        return None
