from flask import session, redirect
from functools import wraps

# expects to receive another function as an argument
def login_required(func):
    # preserves the original name when creating the wrapped function
    @wraps(func)
    # *args and **kwargs keywords ensure that no matter how many arguments are given (if any), 
    # the wrapped_function() captures them all.

    # TODO: add print statements to debug the RuntimeError call, confirm function is called
    def wrapped_function(*args, **kwargs):
        # if logged in, call original function with original arguments
        if session.get('loggedIn') == True:
          return func(*args, **kwargs)

        return redirect('/login')

    return wrapped_function


