
def is_castable(obj, casting_function) -> bool:
    try:
        casting_function(obj)
        return True
    except TypeError:
        return False
    except:
        return True

def is_iterable(obj) -> bool:
    return is_castable(obj, iter)

def is_hashable(obj) -> bool:
    return is_castable(obj, hash)

def is_stringable(obj) -> bool:
    return (type(obj).__str__ is not object.__str__)