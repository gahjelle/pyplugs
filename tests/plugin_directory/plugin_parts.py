import pyplugs


@pyplugs.register
def plugin_default():
    return "default"


@pyplugs.register
def plugin_next():
    return "next"


@pyplugs.register
def plugin_named():
    return "named"


@pyplugs.register
def plugin_last():
    return "last"
