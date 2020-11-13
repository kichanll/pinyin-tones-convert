import os
import sys
import unidecode as ud
import re


yuanyin_list = [
    {"āáǎăà": [{"ā": "1"}, {"á": "2"}, {"ǎ": "3"}, {"ă": "3"}, {"à": "4"}], "yuanyin": "a"},
    {"ōóǒŏò": [{"ō": "1"}, {"ó": "2"}, {"ǒ": "3"}, {"ŏ": "3"}, {"ò": "4"}, ], "yuanyin": "o"},
    {"ēéěĕè": [{"ē": "1"}, {"é": "2"}, {"ě": "3"}, {"ĕ": "3"}, {"è": "4"}, ], "yuanyin": "e"},
    {"īíǐĭì": [{"ī": "1"}, {"í": "2"}, {"ǐ": "3"}, {"ĭ": "3"}, {"ì": "4"}, ], "yuanyin": "i"},
    {"ūúǔŭù": [{"ū": "1"}, {"ú": "2"}, {"ǔ": "3"}, {"ŭ": "3"}, {"ù": "4"}, ], "yuanyin": "u"},
    {"ǖǘǚǜü": [{"ǖ": "1"}, {"ǘ": "2"}, {"ǚ": "3"}, {"ǜ": "4"}, {"ü": ""}], "yuanyin": "v"},
]


def parsed_yin(yin):
    for i in yin:
        if i in "āáǎăàōóǒŏòēéěĕèīíǐĭìūúǔŭùǖǘǚǜü":
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

def create_tone_with_number(input_path, ouput_path):
    if not os.path.exists(input_path):
        print('please double check {}'.format(input_path))
        return

    with open(ouput_path, 'w') as p:
        with open(input_path, 'r') as f:
            for line in f.readlines():
                text, label = line.strip().split('|', maxsplit=1)
                tone_label = []

                for i in eval(eval(label)):
                    t = parsed_yin(i)
                    tone_label.append(t)
                tone_label = repr(repr(tone_label))
                print(text, tone_label)
                p.write('{}|{}\n'.format(text, tone_label))

def main(argv):
    create_tone_with_number(argv[1], argv[2])

if __name__ == '__main__':
    main(sys.argv)
