__all__ = ["public_function"] # only this will get imported in another script when using from 'module' import *

PUBLIC_CONSTANT = "I'm meant to be used"
_PRIVATE_CONSTANT = "I'm internal only"

def public_function():
    return "Use me!"

def _private_helper():
    return "I'm internal"

def another_public():
    return "Alsp public"
