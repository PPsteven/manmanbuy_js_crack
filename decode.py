import re, execjs

def callJsFunc(s, func=""):
    v1, v2 = s.group(1), s.group(2)
    return "'{}'".format(ctx.eval('_0x365d(%s, %s)' %(v1, v2)))

with open("customRequest.js", "r", encoding="utf-8") as fr:
    raw_code = fr.read()
    ctx = execjs.compile(raw_code)

pattern = re.compile(r"_0x365d\(('.*?'), ('.*?')\)", re.S)
trans_code = re.sub(pattern, callJsFunc, raw_code)
with open('customRequest_trans.js', 'w', encoding="utf-8") as fw:
    fw.write(trans_code)
