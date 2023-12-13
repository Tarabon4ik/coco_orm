from typing import Union, Optional
import functools

from PIL import Image


def check_and_fix_img_type(img: Union[Image.Image, bool, None]) -> Optional[Image.Image]:
    """
    Check and fix image type.

    Args:
        img (Union[Image.Image, bool, None]): an image/image attribute.

    Returns:
        Optional[Image.Image]: an image of PIL.Image type if provided, else None
    """
    return None if isinstance(img, bool) else img


def handle_exceptions(func) -> bool:
    """
    Standardize return value of a given function to bool by handling exceptions (with the help of try...except construction).

    Args:
        func (Callable): a function to be called within wrapper.

    Returns:
        bool: True if function execution is successful, False if not (prints exception message).
    """
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        try:
            func(*args, **kwargs)
            return True
        except Exception as e: 
            print(e)
            return False
    return wrapper_decorator