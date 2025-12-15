def format_enum(enum):
    names = enum.name.split('|')
    return ", ".join(name.capitalize() for name in names)
