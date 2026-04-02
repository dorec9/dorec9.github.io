---
title: "데이터 분석/통계"
permalink: /categories/data-statistics/
layout: archive
taxonomy: data-statistics
---

데이터 기반 분석 사례와 통계 방법론을 다룹니다.

{% assign posts = site.categories["data-statistics"] %}
{% for post in posts %}
  {% include archive-single.html type="list" %}
{% endfor %}
