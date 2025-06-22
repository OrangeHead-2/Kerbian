def merge_styles(*styles):
    merged = {}
    for style in styles:
        merged.update(style)
    return merged