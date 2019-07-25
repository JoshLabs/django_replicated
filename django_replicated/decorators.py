# coding: utf-8
'''
Decorators for using specific routing state for particular requests.
Used in cases when automatic switching based on request method doesn't
work.

Usage:

    from django_replicated.decorators import use_master, use_slave

    @use_master
    def my_view(request, ...):
        # master database used for all db operations during
        # execution of the view (if not explicitly overriden).

    @use_slave
    def my_view(request, ...):
        # same with slave connection
'''
from __future__ import unicode_literals

from django.utils.decorators import decorator_from_middleware_with_args

from .utils import routers
from .middleware import ReplicationMiddleware


def use_state_in_function(forced_state='master'):

    def _make_decorator(func):

        def wrapper(*args, **kwargs):
            prev_state = routers.state()  # Store previous state
            routers.init(forced_state)  # Set state to the forced_state
            func(*args, **kwargs)
            # If previous state was master, set it back
            # Handling function calls from other functions or classes
            if prev_state == 'master':
                routers.init('master')
        return wrapper

    return _make_decorator


use_state = decorator_from_middleware_with_args(ReplicationMiddleware)
use_master = use_state(forced_state='master')
use_slave = use_state(forced_state='slave')
use_master_in_function = use_state_in_function()
use_slave_in_function = use_state_in_function(forced_state='slave')
