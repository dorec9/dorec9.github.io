---
title: "프로젝트 회고"
permalink: /categories/project-retrospect/
layout: archive
taxonomy: project-retrospect
---

설계 판단 과정을 중심으로 프로젝트를 복기합니다.

{% assign posts = site.categories["project-retrospect"] %}
{% for post in posts %}
  {% include archive-single.html type="list" %}
{% endfor %}
