print('Sleeping to allow recovery...')
import time

time.sleep(5)
print('Done sleeping. Continuing execution.')

from app import App

app = App()
app.run()
