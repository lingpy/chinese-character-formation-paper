from lingpy import *
from sinopy import *
from collections import defaultdict
import networkx as nx
from classify import *
from tabulate import tabulate
import sys
import html
from collections import defaultdict
from tqdm import tqdm


def load_data(path):

    data = csv2list(path, strip_lines=False)
    out = defaultdict(list)
    for line in data[1:]:
        out[line[0]] +=  [dict(zip([h.lower() for h in data[0]], line))]
    return out

# make a network of all series
def make_graph(data):
    G = nx.DiGraph()
    for char, vals in data.items():
        if vals['xiesheng'] and vals['xiesheng'] != '?':
            if vals['xiesheng'] in G:
                G.node[vals['xiesheng']]['frequency'] += 1
            else:
                G.add_node(vals['xiesheng'], series=vals['karlgren'],
                        frequency=1)

            if char in G:
                G.node[char]['frequency'] += 1
            else:
                G.add_node(char, series=vals['karlgren'], frequency=1)

            if char in G[vals['xiesheng']]:
                G[vals['xiesheng']]['frequency'] += 1
            else:
                G.add_edge(vals['xiesheng'], char, frequency=1)
    return G


if __name__ == '__main__':
    from sys import argv, exit
    data = load_data('data/data.tsv')
    
    if not [x for x in argv if x in ['sagart', 'graph', 'haudricourt', 'starostin',
        'gabelentz', 'pulleyblank', 'pan', 'wang']]:
        exit()

    if 'graph' in argv:

        G = make_graph(data)
        with open('output/graph.gml', 'w') as f:
            for x in nx.generate_gml(G):
                f.write(html.unescape(x)+'\n')
        exit()

    condition3 = initial
    
    if 'sagart' in argv:
        condition1 = sandeng
        condition2 = lambda x: False if sandeng(x) else True
        cname = 'sagart'
        header = ['GROUP', 'MCH',  'B', 'A', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x

    if 'haudricourt' in argv:
        condition1 = final_p
        condition2 = final_t
        cname = 'haudricourt'
        header = ['GROUP', 'MCH',  'p', 't', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x

    if 'wang' in argv:
        condition1 = n_final
        condition2 = has_t
        cname = 'wang'
        header = ['GROUP', 'MCH', 'n', 't', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x

    if 'pulleyblank' in argv:
        condition1 = qutone
        condition2 = lambda x: False if qutone(x) else True
        cname = 'pulleyblank'
        header = ['GROUP', 'MCH',  'qu', 'other', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x

    if 'starostin' in argv:
        condition1 = n_final
        condition2 = no_t_ng #lambda x: False if n_final(x) else True
        cname = 'starostin'
        header = ['GROUP', 'MCH',  'n-final', 'not-n-final', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x

    if 'pan' in argv:
        condition1 = velars
        condition2 = glottals
        cname = 'pan'
        header = ['GROUP', 'MCH', 'velars', 'glottals', 'none', 'PURITY']
        condition = lambda x: '1' in x and (
                not 'm' in x and not 'th' in x and not 'd' in x) and (
                        '2' in x)

    if 'gabelentz' in argv:
        condition1 = velars
        condition2 = lateral
        cname = 'gabelentz'
        header = ['GROUP', 'MCH', 'velars', 'laterals', 'none', 'PURITY']
        condition = lambda x: '1' in x and '2' in x
    
    D = defaultdict(lambda : defaultdict(list))
    text = '<html><head><meta charset="utf-8"/><style>td {border: 1pt solid black};</style> </head><body>'

    # make initial test with the data to share it
    found = 1

    # get karlgren nodes
    karlgren = set()
    for k, vals in data.items():
        for val in vals:
            karlgren.add(val['karlgren'])
    karlgren = sorted(karlgren)

    all_data, all_mch = [], defaultdict(list)
    for k, v in data.items():
        all_data += v
        for val in v:
            all_mch[k] += [val['mch']]

    # iterate over all karlgren items
    for group in tqdm(karlgren, 'analyzing characters'):
        # assemble xiesheng series
        chars = [(x['character'], x['mch'], x['xiesheng']) for x in \
                        all_data if x['karlgren'] == group and
                        x['xiesheng'].strip('?') and x['mch'].strip()
                        ]
            
        for char, mch, xiesheng in chars:
            D[group][xiesheng] += [(char, mch)]

        if chars:
            is_condition = []
            for char, mch, xiesheng in chars:
                if condition1(mch):
                    is_condition += ['1']
                elif condition2(mch):
                    is_condition += ['2']
                else:
                    is_condition += [condition3(mch)]

            table = []
            for xiesheng in D[group].keys():
                row = [xiesheng, ', '.join(all_mch.get(char, [''])), [], [], [], '']
                for char, mch in D[group][xiesheng]:
                    if condition1(mch):
                        row[2] += [char+'<sup>'+str(hex(ord(char)))[2:]+'&nbsp;'+mch+'</sup>']
                    elif condition2(mch):
                        row[3] += [char+'<sup>'+str(hex(ord(char)))[2:]+'&nbsp;'+mch+'</sup>']
                    else:
                        row[4] += [char+'<sup>'+str(hex(ord(char)))[2:]+'&nbsp;'+mch+'</sup>']

                if row[2] and not row[3]:
                    row[5] = 'pure:'+header[2]
                if row[3] and not row[2]:
                    row[5] = 'pure:'+header[3]
                if row[2] and row[3]:
                    row[5] = 'mixed'
                row[2] = '<br>'.join(row[2])
                row[3] = '<br>'.join(row[3])
                row[4] = '<br>'.join(row[4])

                table += [row]

            if condition(is_condition):
                if '--verbose' in argv or '-v' in argv:
                    print(group)
                    print('')
                    print(tabulate(table, headers=header))
                    print('')
                if len(D[group]) > 1:
                    text += '<p>'+'('+str(found)+') '
                    text += group+' [{0}]'.format(len(D[group]))+''
                    text += tabulate(table, headers=header,
                            tablefmt='html').replace(
                                    '<td>', 
                                    '<td style="width:70px; border: 1px solid black">'
                                    ).replace(
                                            '<table>',
                                            '<table style="width:500px;">'
                                            )
                    text += '</p>'
                    found += 1
    with open('output/'+cname+'.html', 'w') as f:
        f.write(text+'</body></html>')


            
