print("\033[91mThis is RED\033[0m")
print("\033[92mThis is GREEN\033[0m")
print("\033[93mThis is YELLOW\033[0m")
print("\033[94mThis is BLUE\033[0m")
print("This is normal")


# =============================================================================
# ANSI COLOR CODES QUICK REFERENCE
# =============================================================================
#
# Pattern: \033[CODEm ... text ... \033[0m
#
# | Code | Color         | Use Case      |
# |------|---------------|---------------|
# | 90   | Gray          | DEBUG         |
# | 91   | Red           | ERROR         |
# | 92   | Green         | SUCCESS/INFO  |
# | 93   | Yellow        | WARNING       |
# | 94   | Blue          | Info/Labels   |
# | 95   | Magenta       | Highlights    |
# | 96   | Cyan          | Debug/Trace   |
# | 0    | Reset         | End of color  |
#
# Bold variants: Add 1; before color (e.g., \033[1;91m = Bold Red)
#
# =============================================================================


import logging

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors based on log level."""
    
    # Color codes for each level
    COLORS = {
        logging.DEBUG: "\033[90m",     # Gray
        logging.INFO: "\033[92m",      # Green
        logging.WARNING: "\033[93m",   # Yellow
        logging.ERROR: "\033[91m",     # Red
        logging.CRITICAL: "\033[1;91m", # Bold Red
    }
    RESET = "\033[0m"
    
    def format(self, record):
        # Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Format the message normally first
        message = super().format(record)
        
        # Wrap with color codes
        return f"{color}{message}{self.RESET}"


# Set up logger with colored output
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create handler with colored formatter
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S'
))
logger.addHandler(handler)

# Test it!
logger.debug("This is debug - gray")
logger.info("This is info - green")
logger.warning("This is warning - yellow")
logger.error("This is error - red")
logger.critical("This is critical - bold red")