
import logging, sys

class Debugging:

    def __init__(self, aName=None):
        self.logname = aName

    def __enter__(self):
        self.default = logging.getLogger(self.logname).getEffectiveLevel() # save old behaviour
        logging.getLogger().setLevel(logging.DEBUG) # set behaviour to also log debugs

    def __exit__(self, exc_type, exc_value, traceback):
        logging.getLogger(self.logname).setLevel(self.default) # re-set old behaviour


print("############### Try Out ###############")
import io
log_file = io.StringIO()

logging.basicConfig(stream=log_file, level=logging.INFO)
logging.info("Before")
logging.debug("Silenced before")
with Debugging():
    logging.info("During")
    logging.debug("Enabled during")
logging.info("Between")
logging.debug("Silenced between")
with Debugging():
   logging.info("Again")
   logging.debug("Enabled Again")
logging.info("Done")
logging.debug("Silenced at the end")
print(log_file.getvalue())
