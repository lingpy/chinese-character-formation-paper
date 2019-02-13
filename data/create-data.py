import re
import lingpy
from sinopy import sinopy
import tqdm

def wikibooks():

    with open('wikibooks.txt') as f:
        data = f.readlines()
    out = []
    gsr = {}
    for i, line in enumerate(data):
        line = line.strip().replace('\t', ' ')
        if line.startswith('*'):
            if not line[1] == ' ':
                line = line.replace('*', '* ')
            elms = line.split(' ')
            if elms and len(elms) > 1:
                kgsc = elms[1].split('/')
                if len(kgsc) == 1:
                    schuessler = ''
                    karlgren = kgsc[0]
                elif len(kgsc) == 2:
                    karlgren = kgsc[1]
                    schuessler = kgsc[0]
                else:
                    print('[ERROR:schuessler/karlgren] {0}'.format(line))
                
                try:
                    char = elms[2].split('|')[-1][0]
                except IndexError:
                    print('[ERROR:character] {0}'.format(line))
                    char = ''
                
                mch = [x[:-1] if x.endswith(',') else x for x in elms[3:]]
                if len(karlgren) not in [4, 5, 6]:
                    print('[ERROR:karlgren] {0}'.format(line, karlgren))
                elif not sinopy.is_chinese(char):
                    print('[ERROR:char] {0}'.format(line))
                elif char:
                    pinyin = sinopy.pinyin(char)
                    if '?' in pinyin or sinopy.is_chinese(pinyin):
                        pinyin = ''
                    out += [(
                        char,
                        pinyin,
                        'Old_Chinese',
                        karlgren[:4],
                        karlgren,
                        '',
                        'Karlgren1954'
                        )]
                    for reading in mch:
                        out += [(
                            char, pinyin, 'Middle_Chinese', '', karlgren, reading,
                            'Wikibooks2016a')]
                        gsr[char] = [pinyin, reading, karlgren]

    with open('karlgren.tsv', 'w') as f:
        f.write('ID\tCHARACTER\tPINYIN\tDOCULECT\tPHONETIC_CLASS\tKARLGREN_ID\tREADING\tSOURCE\n')
        for i, line in enumerate(out):
            f.write(str(i+1)+'\t'+'\t'.join(line)+'\n')
    
    return gsr


def xiesheng():
    with open('ids-analysis.txt') as f:
        comps = {}
        ignored = set()
        for line in f:
            sheng = ''
            cells = [x.strip() for x in line.split('\t')]
            if cells[1] not in comps:
                if len(cells) > 3:
                    cells[3] = cells[3].replace('声', '聲')
                    if cells[3].endswith('聲'):
                        if len(cells[3]) == 2:
                            sheng = cells[3][0]
                        elif len(cells[3]) == 3 and cells[3][1] in ['亦', '省']:
                            sheng = cells[3][0]
                        elif len(cells[3]) == 4:
                            sheng = cells[3][0]
                        else:
                            ignored.add(cells[3])
                            sheng = '?'
                    elif cells[2].startswith('→'):
                        sheng = cells[2]

                    elif cells[3] in [
                            '象形',
                            '簡体', 
                            '會意',
                            '指事',
                            ]:
                        sheng = cells[1]
                    elif cells[2] == cells[1]:
                        sheng = cells[1]
                    else:
                        sheng = '?'

                elif cells[2].startswith('→'):
                    if cells[1] not in comps:
                        sheng = cells[2]


                comps[cells[1]] = sheng

        for a, b in comps.items():
            if b.startswith('→'):
                try:
                    comps[a] = comps[b[1]]
                except KeyError:
                    
                    comps[a] = '?'
                
        for c in ignored:
            print(c)
    return comps

if __name__ == '__main__':

    gsr = wikibooks()
    ids = xiesheng()

    with open('data.tsv', 'w') as f:
        f.write('\t'.join(
            [
                'CHARACTER',
                'KARLGREN',
                'KARLGRENCODE',
                'XIESHENG',
                'PINYIN',
                'MCH'
                ])+'\n')

        missing = 0

        for char, vals in sorted(
                gsr.items(), 
                key=lambda x: (x[1][2], x[1][1])):
            xs = ids.get(char, '')
            if len(xs) > 1:
                missing += 1
                xs = '??'
            elif not xs:
                missing += 1
                xs = '?'
            elif xs == '?':
                missing += 1
            
            f.write('\t'.join([
                char,
                vals[2][:4],
                vals[2][4:],
                xs,
                vals[0],
                vals[1]])+'\n')
    print(missing)
        



