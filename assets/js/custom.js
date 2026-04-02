(function() {
  'use strict';

  // === 스크롤 프로그레스 바 ===
  function initProgressBar() {
    var progressBar = document.getElementById('readingProgress');
    if (!progressBar) return;

    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        window.requestAnimationFrame(function() {
          var scrollTop = window.scrollY || document.documentElement.scrollTop;
          var docHeight = document.documentElement.scrollHeight - window.innerHeight;
          var scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
          progressBar.style.width = scrollPercent + '%';
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  // === Back-to-top 버튼 ===
  function initBackToTop() {
    var btn = document.getElementById('backToTop');
    if (!btn) return;

    var sentinel = document.createElement('div');
    sentinel.style.height = '1px';
    document.body.prepend(sentinel);

    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        btn.classList.toggle('is-visible', !entry.isIntersecting);
      });
    }, {
      rootMargin: '300px 0px 0px 0px'
    });

    observer.observe(sentinel);

    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // === 코드 블록 복사 버튼 ===
  function initCodeCopyButtons() {
    document.querySelectorAll('div.highlighter-rouge, figure.highlight').forEach(function(block) {
      var btn = document.createElement('button');
      btn.className = 'code-copy-btn';
      btn.textContent = '복사';
      btn.setAttribute('aria-label', '코드 복사');
      block.appendChild(btn);

      btn.addEventListener('click', function() {
        var code = block.querySelector('code');
        if (!code) return;

        var text = code.innerText;

        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(function() {
            btn.textContent = '완료!';
            setTimeout(function() { btn.textContent = '복사'; }, 2000);
          }).catch(function() {
            fallbackCopy(text, btn);
          });
        } else {
          fallbackCopy(text, btn);
        }
      });
    });
  }

  function fallbackCopy(text, btn) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      btn.textContent = '완료!';
      setTimeout(function() { btn.textContent = '복사'; }, 2000);
    } catch (e) {
      btn.textContent = '실패';
    }
    document.body.removeChild(textarea);
  }

  // === 이미지 라이트박스 ===
  function initLightbox() {
    var overlay = document.getElementById('lightbox');
    var lightboxImg = document.getElementById('lightboxImg');
    if (!overlay || !lightboxImg) return;

    document.querySelectorAll('.page__content img:not(.author__avatar)').forEach(function(img) {
      img.addEventListener('click', function() {
        lightboxImg.src = this.src;
        lightboxImg.alt = this.alt;
        overlay.classList.add('is-open');
        document.body.style.overflow = 'hidden';
      });
    });

    overlay.addEventListener('click', closeLightbox);
  }

  function closeLightbox() {
    var overlay = document.getElementById('lightbox');
    if (!overlay) return;
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  // === `/` 키 검색 포커스 ===
  function initSearchShortcut() {
    document.addEventListener('keydown', function(e) {
      var tag = e.target.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) {
        return;
      }

      if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        var searchInput = document.querySelector('.search-input') ||
                          document.querySelector('#search') ||
                          document.querySelector('input[type="search"]');
        if (searchInput) {
          searchInput.focus();
        }
      }
    });
  }

  // === Esc 닫기 통합 ===
  function initEscClose() {
    document.addEventListener('keydown', function(e) {
      if (e.key !== 'Escape') return;

      var lightbox = document.getElementById('lightbox');
      if (lightbox && lightbox.classList.contains('is-open')) {
        closeLightbox();
        return;
      }

      var searchInput = document.querySelector('input[type="search"]:focus');
      if (searchInput) {
        searchInput.blur();
      }
    });
  }

  // === 초기화 ===
  document.addEventListener('DOMContentLoaded', function() {
    initProgressBar();
    initBackToTop();
    initCodeCopyButtons();
    initLightbox();
    initSearchShortcut();
    initEscClose();
  });
})();
