from html_mitra import html_mitra as html
main_file =html.create_html("hello.html")
h1 = html.create_element("h1","This is a test site")
html.append(main_file,h1)
html.finish(main_file)