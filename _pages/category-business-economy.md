---
title: "경영·경제 분석"
permalink: /categories/business-economy/
layout: archive
taxonomy: business-economy
---

경영/경제 이슈에 대한 실무적 해석을 기록합니다.

{% assign posts = site.categories["business-economy"] %}
{% for post in posts %}
  {% include archive-single.html type="list" %}
{% endfor %}
