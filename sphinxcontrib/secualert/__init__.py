# -*- coding: utf-8 -*-
"""Package for `secualert` Sphinx extension.
"""
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst import directives
from docutils import nodes

from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from sphinx.util.texescape import tex_escape_map
from sphinx.locale import get_translation
from sphinx.environment import NoUri

import os.path


# Constants  ----------------------------------------------------------------

MODULE_NAME = "secualert"
# This will also be used as POT filename.


# Utilities  ----------------------------------------------------------------

_ = get_translation(MODULE_NAME)


# Nodes  --------------------------------------------------------------------

class secualert_node(nodes.Admonition, nodes.Element):
    pass


class secualertlist_node(nodes.General, nodes.Element):
    pass


# Directives  ---------------------------------------------------------------

class SecuAlertList(SphinxDirective):
    """
    A list of all secu. alert entries.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}  # type: Dict

    def run(self):
        # type: () -> List[todolist]
        # Simply insert an empty todolist node which will be replaced later
        # when process_todo_nodes is called
        return [secualertlist_node('')]


class SecuAlert(BaseAdmonition, SphinxDirective):
    """
    A secu. alert entry, displayed in the form of an admonition.
    """
    node_class = secualert_node
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'class': directives.class_option,
    }

    def run(self):
        if not self.options.get('class'):
            self.options['class'] = ['admonition-secualert']

        (alert,) = super(SecuAlert, self).run()
        if isinstance(alert, nodes.system_message):
            return [alert]

        alert.insert(0, nodes.title(text=_('Security Alert')))
        set_source_info(self, alert)

        targetid = 'index-%s' % self.env.new_serialno('index')
        # Stash the target to be retrieved later in latex_visit_todo_node.
        alert['targetref'] = '%s:%s' % (self.env.docname, targetid)
        targetnode = nodes.target('', '', ids=[targetid])
        return [targetnode, alert]


# Events  -------------------------------------------------------------------

def process_alerts(app, doctree):
    # collect all todos in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env

    if not hasattr(env, 'secualert_all_alerts'):
        env.secualert_all_alerts = []

    for node in doctree.traverse(secualert_node):
        app.emit('secualert-defined', node)

        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        newnode = node.deepcopy()
        del newnode['ids']
        env.secualert_all_alerts.append({
            'docname': env.docname,
            'source': node.source or env.doc2path(env.docname),
            'lineno': node.line,
            'alert': newnode,
            'target': targetnode,
        })


def process_secualertlist_nodes(app, doctree, fromdocname):
    # Replace all secualertlist nodes with a list of the collected alerts.
    # Augment each alert with a backlink to the original location.
    env = app.builder.env

    for node in doctree.traverse(secualertlist_node):
        if node.get('ids'):
            content = [nodes.target()]
        else:
            content = []

        for alert_info in env.secualert_all_alerts:
            para = nodes.paragraph(classes=['secualert-source'])
            description = (
                _('(The <<original entry>> is located in %s, line %d.)') %
                (alert_info['source'], alert_info['lineno'])
            )
            desc1 = description[:description.find('<<')]
            desc2 = description[description.find('>>') + 2:]
            para += nodes.Text(desc1, desc1)

            # Create a reference
            newnode = nodes.reference('', '', internal=True)
            innernode = nodes.emphasis(_('original entry'), _('original entry'))
            try:
                newnode['refuri'] = app.builder.get_relative_uri(
                    fromdocname, alert_info['docname'])
                if 'refid' in alert_info['target']:
                    newnode['refuri'] += '#' + alert_info['target']['refid']
                else:
                    newnode['refuri'] += '#' + alert_info['target']['ids'][0]
            except NoUri:
                # ignore if no URI can be determined, e.g. for LaTeX output
                pass
            newnode.append(innernode)
            para += newnode
            para += nodes.Text(desc2, desc2)

            alert_entry = alert_info['alert']
            # Remove targetref from the (copied) node to avoid emitting a
            # duplicate label of the original entry when we walk this node.
            if 'targetref' in alert_entry:
                del alert_entry['targetref']

            # (Recursively) resolve references in the todo content
            env.resolve_references(alert_entry, alert_info['docname'],
                                   app.builder)

            # Insert into the todolist
            content.append(alert_entry)
            content.append(para)

        node.replace_self(content)


def purge_secualerts(app, env, docname):
    if not hasattr(env, 'secualert_all_alerts'):
        return
    env.secualert_all_alerts = \
        [alert for alert in env.secualert_all_alerts
                                                if alert['docname'] != docname]


def merge_info(app, env, docnames, other):
    if not hasattr(other, 'secualert_all_alerts'):
        return
    if not hasattr(env, 'secualert_all_alerts'):
        env.secualert_all_alerts = []
    env.secualert_all_alerts.extend(other.secualert_all_alerts)


# Visits and departures  ----------------------------------------------------

def visit_secualert_node(self, node):
    self.visit_admonition(node)


def depart_secualert_node(self, node):
    self.depart_admonition(node)


def latex_visit_secualert_node(self, node):
    title = node.pop(0).astext().translate(tex_escape_map)
    self.body.append(u'\n\\begin{sphinxadmonition}{warning}{')
    # If this is the original todo node, emit a label that will be referenced by
    # a hyperref in the todolist.
    target = node.get('targetref')
    if target is not None:
        self.body.append(u'\\label{%s}' % target)
    self.body.append('%s:}' % title)


def latex_depart_secualert_node(self, node):
    self.body.append('\\end{sphinxadmonition}\n')


# Setup  --------------------------------------------------------------------

def setup(app):
    """Sphinx extension initialization.
    """
    app.add_event('secualert-defined')

    # I18n initialization for the extension
    locale_dirpath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'locale')
    app.add_message_catalog(MODULE_NAME, locale_dirpath)

    app.add_node(secualertlist_node)
    app.add_node(secualert_node,
                 html=(visit_secualert_node, depart_secualert_node),
                 latex=(latex_visit_secualert_node, latex_depart_secualert_node),
                 text=(visit_secualert_node, depart_secualert_node),
                 man=(visit_secualert_node, depart_secualert_node),
                 texinfo=(visit_secualert_node, depart_secualert_node))

    app.add_directive('secualert', SecuAlert)
    app.add_directive('secualertlist', SecuAlertList)
    app.connect('doctree-read', process_alerts)
    app.connect('doctree-resolved', process_secualertlist_nodes)
    app.connect('env-purge-doc', purge_secualerts)
    app.connect('env-merge-info', merge_info)

    return {
        'version': '0.1',
        'env_version': 1,
        'parallel_read_safe': True
        }

