from markdown_it import MarkdownIt

with open('finance/bankruptcy-declaration-2017-2023.md', 'r') as f:
    source = f.read()

md = MarkdownIt()
html = md.render(source)

with open('finance/bankruptcy-declaration-2017-2023.html', 'w') as f:
    f.write('<html><head><title>Bankruptcy Declaration</title></head><body>' + html + '</body></html>')
