# Pelican Plugin Markdown Parse

A demonstration of a pelican plugin not parsing internal links (eg:
`{static}/images/...`) properly, when `content` returned from a custom `Reader`
returns markdown instead of html.

Using `pelican==4.2.0`

## How to use
1. Install pelican (or `pip install -r requirements.txt`)
1. Run the server (`pelican --listen`)
1. Browse to http://localhost:8000/remark-test.html and view page source from
   your browser
1. Observe that the `{static}/images/git-status.png` line was not converted
   properly, was is the case in http://localhost:8000/markdown-test.html

## Explanation
There are two articles in this project, `hello.md` and `hello.remark`.

* `hello.md` is the `markdown-test.html` post and uses the default
  MarkdownReader that comes with pelican.
* `hello.remark` is the `remark-test.html` post, and uses a custom reader,
  `RemarkReader` that inherits from `MarkdownReader`. This reader works
identically to that of it's parent class, except that the `content` it returns
is the file contents in markdown form, not converted into HTML (as is the case
with `MarkdownReader`)

For some reason (unknown to me), when articles are being generated, whatever
step comes after the reader step does not correctly replace `{static}` with the
generated location. I'm not sure if this is by design or not.
