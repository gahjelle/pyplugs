import pyplugs


@pyplugs.register(sort_value=10)
def plugin_last():
    return "last"
