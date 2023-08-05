simple-github-crawler Documentation
============================
This is github-crawler package. You can crawl the count of consecutive commits.

Quick Start
===========
```
from simple_github_crawler import commit

is_complted, streak = commit.get_streak(username='JAY-Chan9yu')
print(streak)
```
