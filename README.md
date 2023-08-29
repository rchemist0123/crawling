# Crawling articles easier

Crawling research articles with **Selenium**, **BeautifulSoup** in Python.

Available websites
- [Pubmed](https://pubmed.ncbi.nlm.nih.gov)
- [KMbase](https://kmbase.medric.or.kr)
- [KISS](https://kiss.kstudy.com)

# Chrome driver issues
- Chromedriver usage with `wd.Chrome(service=Service(ChromeDriverManager().install()))` unavailable due to Chrome version (≥115)
- The argument `driver_dir` must be provided.

# How to use
1. Select a crawling site (among the available lists above).
2. Type keyword to `keyword` argument.
3. Run `{}_crawling` function.

# TODO
- [RISS](http://www.riss.kr/index.do)