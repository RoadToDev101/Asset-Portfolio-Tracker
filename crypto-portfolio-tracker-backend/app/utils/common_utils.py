def remove_private_attributes(obj):
    return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
