"""Build ComfyUI UI-format workflow JSON (the format the editor and Comfy Cloud open with a layout)
from a compact description, using the node schemas from a running ComfyUI's /object_info.

Usage in a script:
    g = Graph(object_info)
    n = g.node('LoadImage', title='Source frame', widgets={'image': 'source.png'}, pos=(0, 0))
    g.link(n, 0, other, 'image')
    g.note('...', pos=..., size=...)
    g.save('out.json')
"""
import json, uuid

WIDGET_TYPES = {'INT', 'FLOAT', 'STRING', 'BOOLEAN', 'COMBO'}

class Graph:
    def __init__(self, object_info, version='0.3.0'):
        self.oi = object_info
        self.nodes = []
        self.links = []
        self.groups = []
        self.ver = version
        self._nid = 0
        self._lid = 0

    def _inputs(self, t):
        spec = self.oi[t]['input']
        out = []
        for sec in ('required', 'optional'):
            for name, s in spec.get(sec, {}).items():
                typ = s[0]; opts = s[1] if len(s) > 1 else {}
                if isinstance(typ, list):
                    typ = 'COMBO'
                if typ == 'COMBO' or (isinstance(typ, str) and typ in WIDGET_TYPES):
                    out.append((name, typ, opts, True))
                else:
                    out.append((name, typ, opts, False))
        return out

    def node(self, t, title=None, widgets=None, pos=(0, 0), size=None, color=None, bgcolor=None, mode=0):
        widgets = widgets or {}
        self._nid += 1
        info = self.oi[t]
        inputs = []
        wvals = []
        for name, typ, opts, is_w in self._inputs(t):
            entry = {'name': name, 'type': typ, 'link': None}
            if is_w:
                entry['widget'] = {'name': name}
                val = widgets.get(name, opts.get('default'))
                if val is None:
                    if typ == 'COMBO':
                        raw = info['input'].get('required', {}).get(name) or info['input'].get('optional', {}).get(name)
                        choices = raw[0] if isinstance(raw[0], list) else (raw[1].get('options') if len(raw) > 1 else [])
                        val = choices[0] if choices else ''
                    elif typ == 'INT': val = 0
                    elif typ == 'FLOAT': val = 0.0
                    elif typ == 'BOOLEAN': val = False
                    else: val = ''
                wvals.append(val)
                if opts.get('control_after_generate'):
                    wvals.append('fixed')
            inputs.append(entry)
        if t == 'LoadImage':
            wvals.append('image')
        outputs = []
        names = info.get('output_name') or info['output']
        for typ, nm in zip(info['output'], names):
            outputs.append({'name': nm, 'type': typ, 'links': []})
        n = {
            'id': self._nid, 'type': t, 'pos': [pos[0], pos[1]], 'flags': {}, 'order': self._nid - 1, 'mode': mode,
            'inputs': inputs, 'outputs': outputs,
            'properties': {'Node name for S&R': t, 'cnr_id': 'comfy-core', 'ver': self.ver},
            'widgets_values': wvals,
        }
        if size: n['size'] = list(size)
        if title: n['title'] = title
        if color: n['color'] = color
        if bgcolor: n['bgcolor'] = bgcolor
        self.nodes.append(n)
        return n

    def note(self, text, pos, size=(360, 160), title='Note', color='#3b3b2e', bgcolor='#5a5a3a'):
        self._nid += 1
        n = {'id': self._nid, 'type': 'MarkdownNote', 'pos': [pos[0], pos[1]], 'size': list(size), 'flags': {},
             'order': self._nid - 1, 'mode': 0, 'inputs': [], 'outputs': [], 'title': title, 'properties': {},
             'widgets_values': [text], 'color': color, 'bgcolor': bgcolor}
        self.nodes.append(n)
        return n

    def link(self, src, out_idx, dst, in_name):
        self._lid += 1
        typ = src['outputs'][out_idx]['type']
        try:
            in_idx = next(i for i, e in enumerate(dst['inputs']) if e['name'] == in_name)
        except StopIteration:
            raise KeyError(f"{dst['type']} has no input {in_name}: {[e['name'] for e in dst['inputs']]}")
        dst['inputs'][in_idx]['link'] = self._lid
        src['outputs'][out_idx]['links'].append(self._lid)
        self.links.append([self._lid, src['id'], out_idx, dst['id'], in_idx, typ])
        return self._lid

    def group(self, title, bounding, color='#444'):
        self.groups.append({'id': len(self.groups) + 1, 'title': title, 'bounding': list(bounding), 'color': color,
                            'font_size': 22, 'flags': {}})

    def to_dict(self):
        for n in self.nodes:
            for o in n['outputs']:
                if not o['links']:
                    o['links'] = None
        return {
            'id': str(uuid.uuid4()), 'revision': 0, 'last_node_id': self._nid, 'last_link_id': self._lid,
            'nodes': self.nodes, 'links': self.links, 'groups': self.groups, 'config': {},
            'extra': {'ds': {'scale': 0.7, 'offset': [60, 60]}}, 'version': 0.4,
        }

    def to_api(self):
        """The same graph as an API-format prompt (what the server runs), for validation."""
        prompt = {}
        by_id = {n['id']: n for n in self.nodes}
        link_by_id = {l[0]: l for l in self.links}
        for n in self.nodes:
            if n['type'] == 'MarkdownNote' or n['mode'] == 4:
                continue
            ins = {}
            wv = list(n['widgets_values'])
            wi = 0
            for e in n['inputs']:
                if e['link'] is not None:
                    l = link_by_id[e['link']]
                    ins[e['name']] = [str(l[1]), l[2]]
                    if 'widget' in e:
                        wi += 1
                        if self._has_cag(n['type'], e['name']): wi += 1
                elif 'widget' in e:
                    ins[e['name']] = wv[wi]; wi += 1
                    if self._has_cag(n['type'], e['name']): wi += 1
            prompt[str(n['id'])] = {'class_type': n['type'], 'inputs': ins, '_meta': {'title': n.get('title', n['type'])}}
        return prompt

    def _has_cag(self, t, name):
        spec = self.oi[t]['input']
        for sec in ('required', 'optional'):
            s = spec.get(sec, {}).get(name)
            if s and len(s) > 1 and s[1].get('control_after_generate'):
                return True
        return False

    def save(self, path):
        json.dump(self.to_dict(), open(path, 'w'), indent=1)
