import os
from api import app

if __name__ == '__main__':
    app.run("0.0.0.0", os.getenv("PORT") or 5000)
