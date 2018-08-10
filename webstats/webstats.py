#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

"""
A simple CGI script that shows server's GPU, CPU and memory load on the browser.

Xaratustrah
2016

"""

import subprocess
import re
from flask import Flask
from jinja2 import Template

CMD = [
    'uname -n',
    'uname -mrsv',
    'date',
    'sar -r 1 1',
    'nvidia-smi --query-gpu=gpu_uuid,memory.total,memory.used,memory.free,temperature.gpu,utilization.gpu,utilization.memory --format=csv',
    'sar -P ALL 1 1',
]

HTML_TMPL = """
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>

    <!--Check JavaScript-->

    <noscript>
      <img src="no_js.gif"
    alt="Why did you disable JavaScript? Without JavaScript you can't see the navigation bar."/>
    </noscript>

    <link href="http://thomasf.github.io/solarized-css/solarized-dark.min.css" rel="stylesheet"></link>

    <script>
        setTimeout(function(){window.location.reload(1);}, 4000);
    </script>

    <style>
    mono {
        background-color: gray;
        color: darkred;
        }

    table.resultsTable {
        text-align:center;
        background-color: gray;
        border-collapse: separate;
        border-width: 1px;
        border-spacing: 2px;
        border-style: outset;
        border-color: gray;
        border-style:solid;
        color: darkred;
        }

    table.resultsTable td {
        border-width: 1px;
        padding: 1px;
        border-style: inset;
        border-color: black;
        background-color: gray;
        -moz-border-radius: ;
        }
    </style>

    <!--Here comes the document title-->

    <title>{{title}}</title>

    <a href="https://github.com/xaratustrah/webstats" target="_blank"><img style="position: absolute; top: 0; right: 0; border: 0;"
    src="https://camo.githubusercontent.com/652c5b9acfaddf3a9c326fa6bde407b87f7be0f4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f6f72616e67655f6666373630302e706e67"
    alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png"></a>
  </head>

  <body>
    Server:
    {% if not ok0 %}
    <mono>{{ out0 }}</mono>
    {% else %}
    Failed to run <b><mono>{{ cmd0 }}</mono></b>.
    {% endif %}
    <br/>
    Time:
    {% if not ok2 %}
    <mono>{{ out2 }}</mono>
    {% else %}
    <br/>
    Failed to run <b><mono>{{ cmd2 }}</mono></b>.
    {% endif %}

    <br/>
    OS:
    {% if not ok1 %}
    <mono>{{ out1 }}</mono>
    {% else %}
    Failed to run <b><mono>{{ cmd1 }}</mono></b>.
    {% endif %}

    <br/>
    Memory:
    <br/>
    {% if not ok3 %}
    <p>{{ out3 }}</p>
    {% else %}
    <br/>
    Failed to run <b><mono>{{ cmd3 }}</mono></b>.
    {% endif %}

    <br/>
    GPU:
    <br/>
    {% if not ok4 %}
    <p>{{ out4 }}</p>
    {% else %}
    <br/>
    Failed to run <b><mono>{{ cmd4 }}</mono></b>.
    {% endif %}

    <br/>
    CPU:
    <br/>
    {% if not ok5 %}
    <p>{{ out5 }}</p>
    {% else %}
    <br/>
    Failed to run <b><mono>{{ cmd5 }}</mono></b>.
    {% endif %}

  </body>
</html>

 """


def run_cmd(cmd_string):
    try:
        p = subprocess.Popen(cmd_string.split(),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ok = p.wait()
        out, err = p.communicate()
    except FileNotFoundError:
        out = b''
        err = b''
        ok = True

    return ok, out, err


app = Flask(__name__)


@app.route('/')
def index():
    tmpl = Template(HTML_TMPL)

    ok0, out0, err0 = run_cmd(CMD[0])
    ok1, out1, err1 = run_cmd(CMD[1])
    ok2, out2, err2 = run_cmd(CMD[2])
    ok3, out3, err3 = run_cmd(CMD[3])
    ok4, out4, err4 = run_cmd(CMD[4])
    ok5, out5, err5 = run_cmd(CMD[5])

    out3 = out3.decode('utf-8')
    out3 = out3.replace(' PM', 'PM')  # remoce pesky PM
    out3 = out3[out3.find('\n\n') + 2:out3.rfind('\n')]  # ignore first line
    out3 = out3.replace('\n', '</td></tr><tr><td>')
    if out3.endswith('<tr><td>'):
        out3 = out3[:-8]
    out3 = re.sub(r"\s+", '</td><td>', out3)
    tab_mem = '<table class="resultsTable"><tr><td>' + out3 + '</td></tr></table>'

    out4 = out4.decode('utf-8')
    out4 = out4.replace('\n', '</td></tr><tr><td>')
    if out4.endswith('<tr><td>'):
        out4 = out4[:-8]
    tab_gpu = '<table class="resultsTable"><tr><td>' + \
        out4.replace(',', '</td><td>') + '</table>'

    out5 = out5.decode('utf-8')
    out5 = out5[out5.find('Average'):]  # ignore first line
    out5 = out5.replace('\n', '</td></tr><tr><td>')
    if out5.endswith('<tr><td>'):
        out5 = out5[:-8]
    out5 = re.sub(r"\s+", '</td><td>', out5)
    tab_cpu = '<table class="resultsTable"><tr><td>' + out5 + '</table>'

    html = tmpl.render(title='WebStats',
                       ok0=ok0, err0=err0, out0=out0.decode("utf-8").replace('\n', '<br/>'), cmd0=CMD[0],
                       ok1=ok1, err1=err1, out1=out1.decode("utf-8").replace('\n', '<br/>'), cmd1=CMD[1],
                       ok2=ok2, err2=err2, out2=out2.decode("utf-8").replace('\n', '<br/>'), cmd2=CMD[2],
                       ok3=ok3, err3=err3, out3=tab_mem, cmd3=CMD[3],
                       ok4=ok4, err4=err4, out4=tab_gpu, cmd4=CMD[4],
                       ok5=ok5, err5=err5, out5=tab_cpu, cmd5=CMD[5],
                       )

    return html

# -------------


if __name__ == '__main__':
    app.run(debug=True)
