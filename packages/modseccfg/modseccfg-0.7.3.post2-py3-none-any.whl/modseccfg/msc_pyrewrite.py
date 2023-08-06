# encoding: utf8
# api: modseccfg
# type: function
# category: gui
# title: MSC_PyParser Rewriting
# description: Permanently modify rule declarations in the global *.conf files
# version: 0.1
# depends: python:msc_pyparser (>= 1.1)
# config: -
# license: GNU GPL v2+
# doc: https://github.com/digitalwave/msc_pyparser/
#
# Wrapper GUI around msc_pyparser and a few of the rewriting
# examples. Can be used to modify rule *.conf files in place
# and permanently. Changes are written back to the global
# secrule *.conf files. Appears in the File menu once enabled.
#
#  * Select the files you want to have rewritten.
#  * Optionally set a range to limit the processing to SecRules.
#  * And pick a transform script to apply on each.
#  * Before starting the process, the shown script can be
#    adapted of course.
#  * Notably there will be some output on the console (from
#    which modseccfg was started) for debugging output - running
#    the help script is a good first start to test this out.
#  * The `--dry-run` mode just displays a window for what each
#    file would have been updated to. (Like a test mode, just
#    run without that flag a second time if you want to apply
#    those changes.)
#
# Operation modes:
#
#  * All default snippets only change properties on a rule by
#    rule basis.
#  * Alternatively, there's the block-wise mode, which might allow
#    some msc_parser transform functions to be used literally.
#    Use `# type: block` to mark up such scripts.  Untested.
#  * For more complex tasks (statistics/rule relation/debugging),
#    the real msc_pyparser scripts should be used.
#
# Might be possible to utilize the examples/ from msc_pyparser
# directly, since the Transform function is often suitable
# for direct use as block-wise script.
# 


import re, json, os, copy
from modseccfg import utils, vhosts, icons, ruleinfo, writer
from modseccfg.utils import conf, log, srvroot
import PySimpleGUI as sg
from textwrap import dedent



# inject to main menu
menu_id = "MSC_PyRewriter"
def init(menu, **kwargs):
    menu[0][1].insert(7, menu_id)
def has(name):
    return name == menu_id


scripts = {
    "help/info": """
       # This field should hold a script block that gets evaluated for each rule
       # in any of the specified input files. It can be adapted before running.
       #
       # Some available local vars:
       #  · `r` is the plain msc_pyparser dict for a rule (alias: `d`)
       #        · r["type"] is often "SecRule"
       #        · r["actions"] a list of dicts (alias: `actions`)
       #  · `rule` is a wrapper object with some convenience methods
       #        · rule.id()
       #        · rule.has_tag("app")
       #        · rule.add_tag("my_new_tag")
       #        · for l in rule.find_actions("logdata"):
       #  · `parser` is the current MSCParser instance
       
       print(r)
       #help(rule)
    """,

    "add_tags": """
        if rule.has_tag("OLD"):
            rule.add_tag("NEW")
    """,

    "remove_tags": """
        rule.remove_tag("OWASP/LENGTHY_TAG_NAME/5.7")
    """,
    
    "remove_audit_log": """
        # msc_pyparser/blob/master/examples/example11_remove_auditlog.py
        for a in actions:
            if a['act_name'] == "ctl" and a['act_arg'] == "auditLogParts" and a['act_arg_val'] == "+E":
                actions.remove(a)
    """,

    "add_flag": """
        actions.append({
            'act_name': "nolog",
            'act_arg': "",
            'act_quote': "no_quote",
            'lineno': r["lineno"],
            'act_arg_val': "",
            'act_arg_val_param': "",
            'act_arg_val_param_val': ""
        })
    """,
    
    "beautify": """
        # type: block
        # description: spaces out all rules
        # url: https://github.com/digitalwave/msc_pyparser/blob/master/examples/example07_beautifier.py
        
        self.lineno = 0
        for d in self.data:
            if d['type'] == "SecRule":
                # empty line before the rule
                self.lineno += 1
                d['oplineno'] = self.lineno
                d['lineno'] = self.lineno
                if "actions" in d:
                    aidx = 0
                    last_trans = ""
                    while aidx < len(d["actions"]):
                        if d['actions'][aidx]['act_name'] == "t":
                            # writed_trans could be used to limit the number of actions
                            # to place in one line
                            writed_trans += 1
                            if last_trans == "t":
                                pass
                            else:
                                self.lineno += 1
                        else:
                            self.lineno += 1
                            writed_trans = 0
                        d['actions'][aidx]['lineno'] = self.lineno
                        last_trans = d['actions'][aidx]['act_name']
                        aidx += 1
                # empty line after the rule
                self.lineno += 1
            else:
                d['lineno'] = self.lineno
                self.lineno += 1
    """,
}


class rulewrap():
    """ utility functions to simplify adapting rules and actions """
    
    def __init__(self, r):
        self.r = r

    def has_tag(self, name):
        """ test if rule has given tag: """
        for tag in self.find_action("tag"):
            if tag == name:
                return True

    def add_tag(self, name):
        """ append a new tag: """
        self.r["actions"].append({
            'act_name': "tag",
            'act_arg': name,
            'act_quote': "quotes",
            'lineno': self.r["actions"][-1]['lineno'],
            'act_arg_val': "",
            'act_arg_val_param': "",
            'act_arg_val_param_val': ""
        })
        
    def remove_tag(self, name):
        """ remove action entry for tag:name """
        for a in self.r["actions"]:
            if a['act_name'] == "tag" and a['act_arg'] == name:
                self.r["actions"].remove(a)

    def find_action(self, name):
        """ iterator to find any/all action names:… and return value """
        for a in self.r["actions"]:
            if a["act_name"] == name:
                yield a["act_arg"]

    def id(self):
        """ find_action("id"), return as integer, or None """
        for a in self.r["actions"]:
            if a['act_name'] == "id":
                return int(a['act_arg'])
    
    def within(self, limit):
        id = self.id()
        if not id:
            return False
        if limit.start <= id <= limit.stop:
            return True


class show():
    """ hook to file menu in mainwindow """

    def __init__(self, mainwindow, data, *a, **kw):
    
        conf_ls = [fn for fn,vh in vhosts.vhosts.items() if vh.t == "rules"]

        # vars
        layout = [
            [sg.T("The transformation scripts get applied to any rule within the selected files (and optionally constrained by the rule range).\nThis is meant to update the /usr/share/modsecurity-crs/rules/*.conf files in place.\nWhereas --dry-run will just display the edited file instead of actually saving it back.", font="Sans 10")],
            [sg.T("Rule files"), sg.Listbox(conf_ls, "", k="filenames", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(76,6), background_color="#eee")],
            [sg.T("Rule IDs  "), sg.Input("0-9990000", k="rule_ids", size=(25,1))],
            [sg.T("Transform", font="Sans 12 bold"), sg.Combo(list(scripts.keys()), k="transform", auto_size_text=1, size=(25,1), background_color="#eee", enable_events=True)],
            [sg.Multiline("# select a transform ↑ script", k="script", size=(80,15), font="Monospace 12")],
            [sg.B("Run/Rewrite"), sg.CB("--dry-run", k="dry", default=True), sg.B("Cancel"),
             sg.T("     "), sg.ProgressBar(2000, k="progress", size=(40,10))]
        ]
        
        self.w = sg.Window(layout=layout, title=f"MSC_PyParser rewriting scripts", resizable=1, font="Sans 12", icon=icons.icon)
        mainwindow.win_register(self.w, self.event)
    

    # act on changed widgets or save/close event
    def event(self, event, data):
        if event == "transform":
            self.w["script"].update(dedent(scripts[data["transform"]]).lstrip())
            pass
        elif event in ("Close", "Cancel"):
            self.w.close()
        elif re.match("^\w+://", event):
            os.system("xdg-open %r" % event)
        elif event == "Run/Rewrite":
            self.rewrite(data["filenames"], data["script"], self.range_from_str(data["rule_ids"]), data["dry"])
            if data["dry"]:
                self.w["progress"].update(0)
            else:
                self.w.close()

    def range_from_str(self, str):
        ids = re.match("(\d+)-+(\d+)", str)
        if ids:
            return range(int(ids[1]), int(ids[2]))
    
    def rewrite(self, filenames, script, limit, dry=False):
        from msc_pyparser import MSCParser, MSCWriter, MSCUtils #→ pip3 install msc_pyparser
        p = self.progress(len(filenames))
        p(20)
        for fn in filenames:
            # read
            parser = MSCParser()
            src = srvroot.read(fn)
            parser.parser.parse(src)
            self.data = parser.configlines # alias (msc_pyparser examples)
            p(5)
            # transform block or rule-wise
            if re.search("^#\s*type:\s*block|^\s*for\s+\w+in\s+(self\.data|parser\.configlines):", script, re.M):
                exec(script)
                p(500)
            else:
                for r in parser.configlines:
                    p(2)
                    rule = rulewrap(r)
                    if r["type"] != "SecRule":
                        continue
                    if limit and not rule.within(limit):
                        continue
                    # aliases (msc_pyparser examples)
                    d = r
                    actions = r["actions"]
                    # eval script block
                    exec(script)
                    p(10)
            # write
            writer = MSCWriter(parser.configlines)
            writer.generate()
            src = "\n".join(writer.output)
            if not dry:
                srvroot.write(fn, src)
            else:
                sg.Window(layout=[[sg.Multiline(src, size=(95,35), font="Monospace 12")]], title=fn).read()

    def progress(self, len=10):
        self.p_max = 750 * len
        self.p = 0
        def update(add=1):
            self.p += add
            self.w["progress"].update(self.p, max=self.p_max)
            self.w.read(timeout=1)
        return update
