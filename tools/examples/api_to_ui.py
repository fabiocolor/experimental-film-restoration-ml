"""Turn an API-format ComfyUI prompt (what the server runs) into a UI-format workflow (what the editor
and Comfy Cloud open, with a layout and notes), so that a published recipe can be inspected node by node.

    from api_to_ui import convert
    convert('graph_api.json', 'graph_ui.json', object_info,
            notes=[('What this graph does', '...markdown...'), ...],
            titles={'8': 'Reference to video'},  # optional, by API node id
            colors={'8': '#223'})                 # optional

The UI graph is validated against the API prompt before it is written: every node, widget value and
link has to come back out of the UI graph exactly as it went in (Graph.to_api), or the conversion fails.
"""
import json
from wfbuild import Graph

COLUMN = 440
ROW_GAP = 40


def _height(node_type, n_inputs, widgets, oi):
    h = 70 + 26 * n_inputs
    for name, v in widgets.items():
        if isinstance(v, str) and len(v) > 60:
            h += 120  # a prompt box
    return h


def _autogrow(n, spec, oi):
    """Dynamic (COMFY_AUTOGROW_V3) inputs such as MiniMax H3's ref_images: the editor serialises each used slot as
    an input named '<group>.<prefix><k>' of the template's type, followed by one empty slot."""
    info = oi[spec['class_type']]['input']
    groups = {}
    for sec in ('required', 'optional'):
        for name, s in info.get(sec, {}).items():
            if s[0] == 'COMFY_AUTOGROW_V3':
                groups[name] = s[1]['template']
    if not groups:
        return
    n['inputs'] = [e for e in n['inputs'] if e['name'] not in groups]
    for gname, tpl in groups.items():
        (iname, ispec), = tpl['input']['required'].items()
        prefix = tpl['prefix']
        used = sorted(k for k in spec['inputs'] if k.startswith(gname + '.' + prefix))
        for k in used:
            n['inputs'].append({'name': k, 'type': ispec[0], 'link': None})
        if used:
            n['inputs'].append({'name': f"{gname}.{prefix}{len(used)}", 'type': ispec[0], 'link': None})


def _dynamic_combo(n, spec, oi):
    """COMFY_DYNAMICCOMBO_V3 widgets such as SaveVideo's format: the editor serialises the chosen option's
    nested inputs as '<parent>.<child>' widgets right after the parent, and once more under the bare child name."""
    info = oi[spec['class_type']]['input']
    for sec in ('required', 'optional'):
        for name, s in info.get(sec, {}).items():
            if s[0] != 'COMFY_DYNAMICCOMBO_V3':
                continue
            idx = next(k for k, e in enumerate(n['inputs']) if e['name'] == name)
            widx = sum(1 for e in n['inputs'][:idx + 1] if 'widget' in e)  # position after the parent in widgets_values
            chosen = n['widgets_values'][widx - 1]
            option = next(o for o in s[1]['options'] if o['key'] == chosen)
            children = []
            for csec in ('required', 'optional'):
                for cname, cs in option['inputs'].get(csec, {}).items():
                    cval = spec['inputs'].get(cname, cs[1].get('default') if len(cs) > 1 else None)
                    if cval is None and cs[0] == 'COMFY_DYNAMICCOMBO_V3':
                        cval = cs[1]['options'][0]['key']
                    children.append((cname, cs[0], cval, csec == 'optional'))
            extra_inputs, extra_vals = [], []
            for cname, ctype, cval, opt in children:
                extra_inputs.append({'name': f'{name}.{cname}', 'type': ctype, 'widget': {'name': f'{name}.{cname}'}, 'link': None})
                extra_vals.append(cval)
            for cname, ctype, cval, opt in children:
                e = {'name': cname, 'type': ctype, 'widget': {'name': cname}, 'link': None}
                if opt:
                    e['shape'] = 7
                extra_inputs.append(e)
                extra_vals.append(cval)
            n['inputs'][idx + 1:idx + 1] = extra_inputs
            n['widgets_values'][widx:widx] = extra_vals


def convert(api_path, out_path, oi, notes=(), titles=None, colors=None, note_width=560, api_out=None):
    api = json.load(open(api_path))
    titles = titles or {}
    colors = colors or {}
    ids = list(api.keys())
    # dependency depth: a node sits one column to the right of everything it reads from
    depth = {}

    def d(i):
        if i in depth:
            return depth[i]
        srcs = [v[0] for v in api[i]['inputs'].values() if isinstance(v, list)]
        depth[i] = 0 if not srcs else 1 + max(d(s) for s in srcs)
        return depth[i]

    for i in ids:
        d(i)
    # loaders (no inputs) that only feed one consumer go next to it rather than all in column 0
    cols = {}
    for i in ids:
        cols.setdefault(depth[i], []).append(i)
    g = Graph(oi)
    nodes = {}
    x0 = note_width + 80
    for c in sorted(cols):
        y = 0
        for i in cols[c]:
            spec = api[i]
            widgets = {k: v for k, v in spec['inputs'].items() if not isinstance(v, list)}
            n_in = len(spec['inputs'])
            h = _height(spec['class_type'], n_in, widgets, oi)
            title = titles.get(i) or spec.get('_meta', {}).get('title')
            n = g.node(spec['class_type'], title=title, widgets=widgets, pos=(x0 + c * COLUMN, y),
                       size=(400, h), color=colors.get(i), bgcolor=None)
            _autogrow(n, spec, oi)
            _dynamic_combo(n, spec, oi)
            n['properties']['recipe_id'] = i   # the node's id in the API-format recipe
            nodes[i] = n
            y += h + ROW_GAP
    for i in ids:
        for name, v in api[i]['inputs'].items():
            if isinstance(v, list):
                g.link(nodes[v[0]], v[1], nodes[i], name)
    # notes down the left-hand side
    y = 0
    for title, text in notes:
        lines = text.count('\n') + len(text) // 95 + 1
        h = min(640, 50 + 19 * lines)
        g.note(text, pos=(0, y), size=(note_width, h), title=title)
        y += h + ROW_GAP
    # validation: the UI graph must give back the API prompt
    back = g.to_api()
    newid = {i: str(nodes[i]['id']) for i in ids}
    for i in ids:
        a = api[i]
        b = back[newid[i]]
        assert a['class_type'] == b['class_type'], (i, a['class_type'], b['class_type'])
        for name, v in a['inputs'].items():
            bv = b['inputs'].get(name)
            if isinstance(v, list):
                assert bv == [newid[v[0]], v[1]], (i, name, v, bv)
            else:
                assert bv == v, (i, name, v, bv)
        extra = set(b['inputs']) - set(a['inputs'])
        if extra:  # widgets the recipe left at their defaults; the UI graph makes them explicit
            print(f'  {api_path}: node {i} {a["class_type"]} defaults made explicit: ' + ', '.join(f'{k}={b["inputs"][k]!r}' for k in sorted(extra)))
    g.save(out_path)
    if api_out:
        json.dump(back, open(api_out, 'w'), indent=1)
    return g
