---
title: "트렌드 리서치"
permalink: /categories/trend-research/
layout: archive
taxonomy: trend-research
---

업계 동향과 기술 트렌드를 조사·정리합니다.

{% assign posts = site.categories["trend-research"] %}
{% for post in posts %}
  {% include archive-single.html type="list" %}
{% endfor %}
