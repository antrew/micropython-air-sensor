RECOVERY_SLEEP_SECONDS = 5

print('Sleeping for', RECOVERY_SLEEP_SECONDS, 'seconds to allow recovery...')
import time

time.sleep(RECOVERY_SLEEP_SECONDS)
print('Done sleeping. Continuing execution.')

from app import App

try:
    app = App()
    app.init()
    app.loop()
except Exception as exception:
    print('Error initializing or looping', exception)
finally:
    app.deepsleep()
