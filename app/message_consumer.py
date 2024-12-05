# File: /home/mohammad/E-commerce-1/app/message_consumer.py
from app.messaging import consume_messages
from app.extensions import logger
import cProfile
import pstats
import io
import os  # Import os module

def handle_message(message):
    """Process the received message."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Existing message processing logic
    logger.info(f"Processing message: {message}")
    # Example processing (replace with actual logic)
    # process_message(message)
    
    profiler.disable()
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(10)  # Top 10 functions
    profiling_info = s.getvalue()
    
    logger.info(f"Profiling info for message processing:\n{profiling_info}")

if __name__ == "__main__":
    consume_messages(handle_message)
