RECOVERY_SLEEP_SECONDS = 5

print('Sleeping for', RECOVERY_SLEEP_SECONDS, 'seconds to allow recovery...')
import time

time.sleep(RECOVERY_SLEEP_SECONDS)
print('Done sleeping. Continuing execution.')

from app import App

app = App()
app.loop()
app.deepsleep()
