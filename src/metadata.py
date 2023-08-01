from datetime import datetime

#[===============================================]

class Vstatic():

    def version():
        return "1.2.0"

    def releasenotes():
          release_notes = f"""
            <ul>
                <li>Added embedded self session logging for new debug report option in about window</li>
                <li>Improved the About window</li>
                <li>Added contact information for bug reporting</li>
                <li>Code clean up</li>
                <li>Fixed 3 minor bugs</li>
                <li>First stable release!</li>
            </ul>
            """
          return release_notes

    def internal_release_status():
        return "Default, Stable"


#[===============================================]

dbgReport_cumulitive = ""

class debug():

    def __init__(self):
        return dbgReport_cumulitive


    def get_log():
        debug_static = f"""

[==================================]\n
Version: {Vstatic.version()}
Flatpak: True
UI version: 2
Internal status: {Vstatic.internal_release_status()}"""
        final_report = debug_static + f"\n\n[==================================]\n\nRun Log from {datetime.utcnow()}:\n\n" + debug.read()
        print(final_report)
        return final_report

    global dbgReport_cumulitive

    def read():
        global dbgReport_cumulitive
        return dbgReport_cumulitive

    def report(input_string, newline=True, line_prompt=True):
        global dbgReport_cumulitive
        if line_prompt:
            dbgReport_cumulitive += "    >>> "
        dbgReport_cumulitive += str(input_string)
        if newline:
            dbgReport_cumulitive += "\n"

    def flush():
        global dbgReport_cumulitive
        dbgReport_cumulitive = ""

    def newline():
        global dbgReport_cumulitive
        dbgReport_cumulitive += "\n"

