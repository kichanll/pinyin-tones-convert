# Pinyin tones convert

convert "zhōng", "guó", "nín", "hǎo"  
to "zhong1", "guo2", "nin2", "hao3"

## Usage
---

```shell
$ git clone git@github.com:kichanll/pinyin-tones-convert.git
$ cd pinyin-tones-convert
$ python pinyin_tone.py test.csv test_after.csv
$ cat test_after.csv
我忘也不能忘，我爱也不能爱 "['wo3', 'wang4', 'ye3', 'bu4', 'neng2', 'wang4', 'wo3', 'ai4', 'ye3', 'bu4', 'neng2', 'ai4']"
拼音真的不难的 "['pin1', 'yin1', 'zhen1', 'de5', 'bu4', 'nan2', 'de5']"
男子汉留汗不流泪 "['nan2', 'zi3', 'han4', 'liu2', 'han4', 'bu4', 'liu2', 'lei4']"
忽略那边的绿色 "['hu1', 'lue4', 'na4', 'bian1', 'de5', 'lv4', 'se4']"
```