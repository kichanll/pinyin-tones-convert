import os
import sys
import unidecode as ud
import re


yuanyin_list = [
    {u"āáǎăà": [{u"ā": "1"}, {u"á": "2"}, {u"ǎ": "3"}, {u"ă": "3"}, {u"à": "4"}], u"yuanyin": u"a"},
    {u"ōóǒŏò": [{u"ō": "1"}, {u"ó": "2"}, {u"ǒ": "3"}, {u"ŏ": "3"}, {u"ò": "4"}, ], u"yuanyin": u"o"},
    {u"ēéěĕè": [{u"ē": "1"}, {u"é": "2"}, {u"ě": "3"}, {u"ĕ": "3"}, {u"è": "4"}, ], u"yuanyin": u"e"},
    {u"īíǐĭì": [{u"ī": "1"}, {u"í": "2"}, {u"ǐ": "3"}, {u"ĭ": "3"}, {u"ì": "4"}, ], u"yuanyin": u"i"},
    {u"ūúǔŭù": [{u"ū": "1"}, {u"ú": "2"}, {u"ǔ": "3"}, {u"ŭ": "3"}, {u"ù": "4"}, ], u"yuanyin": u"u"},
    {u"ǖǘǚǜü": [{u"ǖ": "1"}, {u"ǘ": "2"}, {u"ǚ": "3"}, {u"ǜ": "4"}, {u"ü": ""}], u"yuanyin": u"v"},
    {u"ńň": [{u"ń": "2"}, {u"ň": "3"}], u"yuanyin": u"n"},
    {u"": [{u"": "2"}], u"yuanyin": u"m"},
    {u"ḿ": [{u"ḿ": "2"}], u"yuanyin": u"m"},
]

pinyinToneMarks = {
    u'a': u'āáǎà', u'e': u'ēéěè', u'i': u'īíǐì',
    u'o': u'ōóǒò', u'u': u'ūúǔù', u'ü': u'ǖǘǚǜ',
    u'n': u' ńň ', u'm': u' ḿ  ',   # ḿ
}


def parsed_yin(yin):
    for i in yin:
        if i in "āáǎăàōóǒŏòēéěĕèīíǐĭìūúǔŭùǖǘǚǜüńňḿ":
            for yuanyin in yuanyin_list:
                for key in yuanyin.keys():
                    if i in key:
                        yuanyin_dic_list = yuanyin.get(key)
                        for dic in yuanyin_dic_list:
                            if i in dic:
                                yuanyin_ = yuanyin.get("yuanyin")
                                yin = yin.replace(i, yuanyin_)
                                num = dic.get(i)
                                yin = yin + str(num)
    yin = yin if re.match('[1-4]', yin[-1]) else yin + '5'
    return yin


def parsed_yin2(yin):
    m = re.search(r'([a-z]*?)([aeiouüv]{1,3})(n?g?r?)([12345])', yin)
    if 'lastindex' in dir(m) and m.lastindex > 2:
        seg = m.group(2).replace(u'v', u'ü')
    else:
        m = re.search(r'([nmsz])(h?g?)([12345])', yin)
        if 'lastindex' in dir(m) and m.lastindex > 2:
            tone = int(m.group(3)) % 5
            pos = 0

            if tone and m.group(1)[pos] in pinyinToneMarks and pinyinToneMarks[m.group(1)[pos]][tone-1] != ' ':
                seg = m.group(1)[:pos] + pinyinToneMarks[m.group(1)[pos]][tone-1] + m.group(1)[pos+1:]
            else:
                seg = m.group(1)

            return seg + m.group(2)

    tone = int(m.group(4)) % 5
    pos = 0
    if len(seg) > 1 and not seg[0] in 'aeo':
        pos = 1
    if tone != 0:
        seg = seg[0:pos] + pinyinToneMarks[seg[pos]][tone-1] + seg[pos+1:]
    return m.group(1) + seg + m.group(3)


def tone_convert(input_path, ouput_path, numeric=True):
    if not os.path.exists(input_path):
        print('please double check {}'.format(input_path))
        return

    with open(ouput_path, 'w') as p:
        with open(input_path, 'r') as f:
            for line in f.readlines():
                text, label = line.strip().split('|', maxsplit=1)
                yin_label = []

                for i in eval(eval(label)):
                    if numeric:
                        t = parsed_yin(i)
                    else:
                        t = parsed_yin2(i)
                    yin_label.append(t)
                yin_label = repr(repr(yin_label))
                p.write('{}|{}\n'.format(text, yin_label))


def main(argv):
    assert len(argv) == 4, 'argv len must be 4. Example:' \
                           'python pinyin_tone.py test.csv test_after.csv test_revert.csv'
    tone_convert(argv[1], argv[2], numeric=True)
    tone_convert(argv[2], argv[3], numeric=False)


if __name__ == '__main__':
    main(sys.argv)
