---
title: "직무 인사이트"
permalink: /categories/planning-insight/
layout: archive
taxonomy: planning-insight
---

경영기획·IT기획 직무 관련 실무 인사이트를 정리합니다.

{% assign posts = site.categories["planning-insight"] %}
{% for post in posts %}
  {% include archive-single.html type="list" %}
{% endfor %}
