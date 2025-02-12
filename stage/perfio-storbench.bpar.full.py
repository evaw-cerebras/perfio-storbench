#!/usr/bin/env python3
'''
[───────────────────────────────────────────────────────────────────────────────]
[ Purpose    ─» Block Storage Analysis: bench, plot, analyze, report [BPAR]
[ Filename   ─» perfio-storbench.bpar.full.py
[ Project    ─» PerfIO-StorBench
[ Author     ─» Eva Winterschön
[ License    ─» BSD-6-Clause
[ Date-INIT  ─» 2024-0802
[ Date-RMOD  ─» 2024-1110
[ Version    ─» 0.4.6
[───────────────────────────────────────────────────────────────────────────────]
[ Requires
[ ╰───────────» python3
[           ╰─» jinja2
[           ╰─» jinja2-cli
[           ╰─»
[───────────────────────────────────────────────────────────────────────────────]
[ References
[ ╰───────────» ⌄unten⌄
[ • PEP-008  ─» [PEP-8 Style Guide](https://peps.python.org/pep-0008/)
[ • PEP-257  ─» [Docstrings Ref](https://peps.python.org/pep-0257/)
[ • PEP-324  ─» [SubProcess Module](https://peps.python.org/pep-0324/)
[ • Doc-Sig  ─» [Py Docs](https://www.python.org/community/sigs/current/doc-sig/)
[───────────────────────────────────────────────────────────────────────────────]
'''
# Erforderlich Modules
import argparse
import jinja2
import os
import psutil
import shutil
import subprocess
import sys

# Validate src-layout import adjustment
if not __package__:
    '''
    Check if using 'src-layout' hierarchy method of app development, if so then
    adjust import path to ensure functionality if called via 'src/package'
    https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
    '''
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

# @decoratorSoSchönen
def proc_vollstreckerin():
    '''
    [───────────────────────────────────────────────────────────────────────────]
    [ Artikel   ─» proc_vollstreckerin || proc_exec
    [ Arbeite   ─» execute cmd via subprocess, provide result
    [ Antworter ─» resp/res tuple from subprocess module
    [───────────────────────────────────────────────────────────────────────────]
    [ Eingabe
    [ • exec_cmd ─» command to execute
    [ • exec_opt ─» command options
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
    [ Antwort
    [ • ret_exec_code ─» execution return code
    [ • ret_exec_zeit ─» execution time total
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
    '''


# @decoratorSoSchönen
def proc_manager():
    '''
    [───────────────────────────────────────────────────────────────────────────]
    [ Artikel   ─» proc_manager
    [ Arbeite   ─» manages threads, workers, queues, pub-sub, database
    [ Antworter ─» response(s)
    [───────────────────────────────────────────────────────────────────────────]
    [ Eingabe
    [ • input-var ─» desc
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
    [ Antwort
    [ • ret-var ─» desc
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
    '''


# @decoratorSoSchönen
def func_j2_render(file_j2=None,file_wr=None):
    '''
    [───────────────────────────────────────────────────────────────────────────]
    [ Artikel   ─» func_j2_render
    [ Arbeite   ─» renders a jinja2 template file
    [ Antworter ─» render status
    [───────────────────────────────────────────────────────────────────────────]
    [ Eingabe
    [ • file_j2 ─» filename for incoming template
    [ • file_wr ─» filename for render output
    [───────────────────────────────────────────────────────────────────────────]
    [ Antwort
    [ • resp_code ─» return the execit code from rendering process
    [ • resp_time ─» return the total time required for rendering
    [───────────────────────────────────────────────────────────────────────────]
    [ https://jinja.palletsprojects.com/en/stable/api/#jinja2.FileSystemLoader
    [───────────────────────────────────────────────────────────────────────────]
    '''

    j2_loader = jinja2.FileSystemLoader(searchpath="./")
    j2_env = jinja2.Environment(loader=j2_loader)
    template = templateEnv.get_template(file_j2)
    outputText = template.render()

    print(outputText)



if __name__ == '__main__':
    ''' DEBUG: echo args if passed to script '''
    print(sys.argv)

    '''
    Since we're not building an exec object'ifier, we'll use dirty arg-seq tedium
    '''
    preflight_bin = "date"
    preflight_opt = "+'%Y.%m.%d %H:%M:%S UTC%z'"
    preflight_cmd = [("%s" %preflight_bin),("%s" %preflight_opt)]

    try:
        completed = subprocess.run(preflight_cmd,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   )
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)

    else:
        print('returncode:', completed.returncode)
        print('DEBUG: {} bytes in stdout: {!r}'.format(
            len(completed.stdout),
            completed.stdout.decode('utf-8'))
            )
        print('DEBUG: {} bytes in stderr: {!r}'.format(
            len(completed.stderr),
            completed.stderr.decode('utf-8'))
            )


    #jinja2 --outfile
    #perfio-storbench.bench-fio.baseline-validate.j2conv.ini perfio-storbench.bench-fio.baseline-validate.ini.j2


'''
[───────────────────────────────────────────────────────────────────────────────]
[ docstring formatting elements copy/paste
[ ╰───────────»
[           ╰─»
[ • PEP-000  ─»
[ • LinkName ─» [Description](URL)
[ •
[ ─»
[ ⌄unten⌄
[───────────────────────────────────────────────────────────────────────────────]

Function docstring iso-de
    [───────────────────────────────────────────────────────────────────────────]
    [ Artikel   ─» func name
    [ Arbeite   ─» work to do
    [ Antworter ─» response(s)
    [───────────────────────────────────────────────────────────────────────────]
    [ Eingabe
    [ • input-var ─» desc
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
    [ Antwort
    [ • ret-var ─» desc
    [ •  ─»
    [───────────────────────────────────────────────────────────────────────────]
'''
