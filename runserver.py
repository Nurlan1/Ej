# -*- coding: utf-8 -*-
from action import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True, debug=True)