import pathlib
p = pathlib.Path(r'c:\Users\yoann\Desktop\Rapport\backend\app\templates\report_detail.html')
text = p.read_text(encoding='utf-8')
idx = text.find('document.getElementById("form-task")')
print(repr(text[idx:idx+700]))
