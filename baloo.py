__kupfer_name__ = _("Baloo")
#__kupfer_sources__ = ("BalooSource", )
__kupfer_actions__ = ("BalooSearch", )
__kupfer_version__ = _("0.0.1")
__kupfer_author__ = _("Richard van Berkum")

from kupfer.objects import Source, TextLeaf, Action, FileLeaf
import subprocess
import re

class BalooSearch(Action):

    def __init__(self):
        super(BalooSearch, self).__init__(_("Search With Baloo"))

    def is_factory(self):
        return True

    def activate(self, leaf):
        return BalooSource(leaf.object)

    def item_types(self):
        yield TextLeaf

    def get_description(self):
        return _("Search with Baloo")

    def get_icon_name(self):
        return "edit-find"

class BalooSource(Source):

    def __init__(self, query):
        super(BalooSource, self).__init__(_("Results for %s") % query)
        self.query = query
        self.ansi_escape = re.compile(r"\x1b[^m]*m")


    def get_items(self):

        p = subprocess.Popen(["baloosearch %s" %self.query], shell=True, stdout=subprocess.PIPE)
        filenames  = p.stdout.readlines()
        filenames = [i for i in filenames if i != "\n"]
        for file in filenames:
            #filename = self.ansi_escape.sub("", file).strip().split(" ", 1)[1]
            filename = file.strip("\n")
            yield FileLeaf(filename)

    def repr_key(self):
        return self.query

    def get_icon_name(self):
        return "edit-find"

