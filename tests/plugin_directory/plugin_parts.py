import pyplugs


@pyplugs.register
def plugin_default():
    return "default"


@pyplugs.register
def plugin_next():
    return "next"


@pyplugs.register
def plugin_final():
    return "final"
