"""Collates and generates foot-notes. Call the macro with the
foot-note content as the only argument:
{{{
   [[FootNote(This is a footnote)]]
}}}
Foot-notes are numbered by the order in which they appear. To create a
reference to an existing foot-note, pass the footnote number as
argument to the macro:
{{{
   [[FootNote(1)]]
}}}
In addition, identical foot-notes are coalesced into one entry. The
following will generate one footnote entry with two references: 
{{{
   Some text[[FootNote(A footnote)]] and some more text [[FootNote(A footnote)]].
}}}
A list of footnotes generated by one or more of the above commands is
produced by calling the macro without arguments: 
{{{
   [[FootNote]]
}}}
Once a set of footnotes has been displayed, a complete new set of
footnotes can be created. This allows multiple sets of footnotes per
page.

"""

from StringIO import StringIO
from trac.util import escape
from trac.wiki import wiki_to_oneliner

def unescape(text):
    """Un-escapes &, <, > and \""""
    if not text:
        return ''
    return unicode(text).replace('&amp;', '&') \
        .replace('&lt;', '<') \
        .replace('&gt;', '>') \
        .replace('&#34;', '"')

def execute(hdf, args, env):
    if not hasattr(hdf, 'footnotes'):
        hdf.footnotes = []
        hdf.footnote_set = 1
    # Display and clear footnotes...
    if not args:
        out = StringIO()
        out.write('<div class="footnotes">\n');
        out.write('<hr style="width: 10%; padding: 0; margin: 2em 0 1em 0;"/>\n');
        out.write('<ol style="padding: 0 0 0 1em; margin: 0;">\n')
        for i, v in enumerate(hdf.footnotes):
            id = "%i.%i" % (hdf.footnote_set, i + 1)
            out.write('<li style="list-style: none;" id="FootNote%s"><a style="font-weight: bold;" href="#FootNoteRef%s">%i.</a> %s</li>\n' % (id, id, i + 1, wiki_to_oneliner(unescape(v), env)))
        out.write('</ol>\n')
        out.write('</div>\n');
        hdf.footnotes = []
        hdf.footnote_set += 1
        return out.getvalue()
    else:
        id = len(hdf.footnotes) + 1
        try:
            id = int(args)
        except ValueError:
            existing = None
            for index, note in enumerate(hdf.footnotes):
                if args == note:
                    existing = note
                    id = index + 1
                    break
            if not existing:
                hdf.footnotes.append(args)
        full_id = "%i.%i" % (hdf.footnote_set, id)
        return '<sup><a title="%s" style="font-size: 8pt; font-weight: bold;" id="FootNoteRef%s" href="#FootNote%s">%i</a></sup>' % (args[:16] + u"...", full_id, full_id, id)