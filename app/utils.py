# File: /home/mohammad/E-commerce-1/app/utils.py
import cProfile
import pstats
import io
from app.extensions import logger
from flask import request

def profile_route(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(10)  # Adjust the number of functions to display
        profiling_info = s.getvalue()
        
        logger.info(f"Profiling info for {request.path}:\n{profiling_info}")
        
        return result
    wrapper.__name__ = func.__name__
    return wrapper
