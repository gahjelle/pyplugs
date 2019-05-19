import pyplugs


@pyplugs.register(sort_value=-10)
def plugin_first():
    return "first"
