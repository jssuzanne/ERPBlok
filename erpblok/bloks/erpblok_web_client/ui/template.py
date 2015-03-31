from anyblok import Declarations
from lxml import html
from copy import deepcopy
from logging import getLogger

logger = getLogger(__name__)


@Declarations.register(Declarations.Exception)
class TemplateException(Exception):
    pass


@Declarations.register(Declarations.Model.UI)
class Template:

    def __init__(self, *args, **kwargs):
        super(Template, self).__init__(*args, **kwargs)
        self.clean()

    def clean(self):
        self.compiled = {}
        self.known = {}

    def get_all_template(self):
        res = []
        for tmpl in self.compiled.keys():
            res.append(self.get_template(tmpl))

        res = '<templates>%s</templates>' % ''.join(res)
        return res.strip()

    def get_template(self, name):
        tmpl = self.compiled[name]
        res = html.tostring(tmpl)
        return res.decode("utf-8").replace('__request_operator__=', '?=')

    def load_file(self, openedfile):
        try:
            el = openedfile.read()
            # the operator ?= are cut, then I replace them before
            # to save the operator in get_template
            el = el.replace('?=', '__request_operator__=')
            element = html.fromstring(el)
        except Exception:
            logger.error('error durring load of %r' % openedfile)
            raise

        if element.tag.lower() == 'template':
            self.load_template(element)
        elif element.tag.lower() == 'templates':
            for _element in element.getchildren():
                print(_element)
                if _element.tag.lower() == 'template':
                    self.load_template(_element)
                else:
                    raise TemplateException(
                        "Only 'template' can be loaded not %r in file %r" % (
                            _element.tag, openedfile))

        else:
            raise TemplateException(
                "Only 'template' or 'templates' can be loaded not %r in %r"
                % (element.tag, openedfile))

    def load_template(self, element):
        name = element.attrib.get('id')
        extend = element.attrib.get('t-extend')
        rewrite = bool(eval(element.attrib.get('rewrite', "False")))

        if name:
            if self.known.get(name) and not rewrite:
                raise TemplateException("Alredy existing template %r" % name)

            self.known[name] = {'tmpl': []}

        if extend:
            if name:
                self.known[name]['extend'] = extend
            else:
                if extend not in self.known:
                    raise TemplateException(
                        "Extend an unexisting template %r" %
                        html.tostring(element))
                name = extend

        if not name:
            raise TemplateException(
                "No template id or extend attrinute found %r" % (
                    html.tostring(element)))

        els = [element] + element.findall('*')
        for el in els:
            if el.text:
                el.text = el.text.strip()

        self.known[name]['tmpl'].append(element)

    def get_xpath(self, element):
        res = []
        for el in element.findall('xpath'):
            res.append(dict(
                expression=el.attrib.get('expression', '/'),
                mult=bool(eval(el.attrib.get('mult', 'False'))),
                action=el.attrib.get('action', 'insert'),
                elements=el.getchildren()))

        return res

    def xpath(self, name, expression, mult):
        tmpl = self.compiled[name]
        if mult:
            return tmpl.findall(expression)
        else:
            return [tmpl.find(expression)]

    def xpath_insert(self, name, expression, mult, elements):
        els = self.xpath(name, expression, mult)
        for el in els:
            nbchildren = len(el.getchildren())
            for i, subel in enumerate(elements):
                el.insert(i + nbchildren, subel)

    def xpath_insertBefore(self, name, expression, mult, elements):
        els = self.xpath(name, expression, mult)
        parent_els = self.xpath(name, expression + '/..', mult)
        for parent in parent_els:
            for i, cel in enumerate(parent.getchildren()):
                if cel in els:
                    for j, subel in enumerate(elements):
                        parent.insert(i + j, subel)

    def xpath_insertAfter(self, name, expression, mult, elements):
        els = self.xpath(name, expression, mult)
        parent_els = self.xpath(name, expression + '/..', mult)
        for parent in parent_els:
            for i, cel in enumerate(parent.getchildren()):
                if cel in els:
                    for j, subel in enumerate(elements):
                        parent.insert(i + j + 1, subel)

    def xpath_remove(self, name, expression, mult):
        els = self.xpath(name, expression, mult)
        parent_els = self.xpath(name, expression + '/..', mult)
        for parent in parent_els:
            for cel in parent.getchildren():
                if cel in els:
                    parent.remove(cel)

    def xpath_replace(self, name, expression, mult, elements):
        els = self.xpath(name, expression, mult)
        parent_els = self.xpath(name, expression + '/..', mult)
        for parent in parent_els:
            for i, cel in enumerate(parent.getchildren()):
                if cel in els:
                    parent.remove(cel)
                    for j, subel in enumerate(elements):
                        parent.insert(i + j, subel)

    def xpath_attributes(self, name, expression, mult, attributes):
        els = self.xpath(name, expression, mult)
        for el in els:
            for k, v in attributes.items():
                el.set(k, v)

    def get_xpath_attributes(self, elements):
        res = []
        for el in elements:
            if el.tag != 'attribute':
                logger.warning(
                    "get %r node, waiting 'attribute' node" % el.tag)
                continue

            res.append(dict(el.items()))

        return res

    def compile_template(self, name):
        if name in self.compiled:
            return self.compiled[name]

        extend = self.known[name].get('extend')

        if extend:
            tmpl = deepcopy(self.compile_template(extend))
            elements = self.known[name]['tmpl']
        else:
            tmpl = self.known[name]['tmpl'][0]
            elements = self.known[name]['tmpl'][1:]

        self.compiled[name] = tmpl

        for el in elements:
            for val in self.get_xpath(el):
                action = val['action']
                expression = val['expression']
                mult = val['mult']
                els = val['elements']
                if action == 'insert':
                    self.xpath_insert(name, expression, mult, els)
                elif action == 'insertBefore':
                    self.xpath_insertBefore(name, expression, mult, els)
                elif action == 'insertAfter':
                    self.xpath_insertAfter(name, expression, mult, els)
                elif action == 'replace':
                    self.xpath_replace(name, expression, mult, els)
                elif action == 'remove':
                    self.xpath_remove(name, expression, mult)
                elif action == 'attributes':
                    for attributes in self.get_xpath_attributes(els):
                        self.xpath_attributes(
                            name, expression, mult, attributes)
                else:
                    raise TemplateException("Unknown action %r" % action)

        return self.compiled[name]

    def compile(self):
        for tmpl in self.known.keys():
            self.compile_template(tmpl)
