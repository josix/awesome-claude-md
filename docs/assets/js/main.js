// Search and Filter functionality for awesome-claude-md

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const categoryFilters = document.querySelectorAll('.filter-btn[data-category]');
  const languageFilters = document.querySelectorAll('.filter-btn[data-language]');
  const exampleCards = document.querySelectorAll('.example-card');
  const resultsCount = document.getElementById('results-count');
  const noResults = document.getElementById('no-results');
  const backToTop = document.getElementById('back-to-top');
  const searchClear = document.getElementById('search-clear');
  const keyboardShortcut = document.getElementById('keyboard-shortcut');
  const activeFiltersContainer = document.getElementById('active-filters');

  let activeCategory = 'all';
  let activeLanguage = 'all';
  let searchQuery = '';
  let debounceTimer;

  // Detect OS for keyboard shortcut display
  if (keyboardShortcut) {
    const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0 ||
                  navigator.userAgent.toUpperCase().indexOf('MAC') >= 0;
    keyboardShortcut.textContent = isMac ? '⌘K' : 'Ctrl+K';
  }

  // Initialize from URL parameters
  initFromURL();

  // Search functionality with debouncing
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        searchQuery = e.target.value.toLowerCase().trim();
        filterExamples();
        updateURL();
        updateClearButton();
      }, 150);
    });
  }

  // Clear search button
  if (searchClear) {
    searchClear.addEventListener('click', function() {
      if (searchInput) {
        searchInput.value = '';
        searchQuery = '';
        filterExamples();
        updateURL();
        updateClearButton();
        searchInput.focus();
      }
    });
  }

  // Category filter
  categoryFilters.forEach(btn => {
    btn.addEventListener('click', function() {
      categoryFilters.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      activeCategory = this.dataset.category;
      filterExamples();
      updateURL();
      updateActiveFilters();
    });
  });

  // Language filter
  languageFilters.forEach(btn => {
    btn.addEventListener('click', function() {
      languageFilters.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      activeLanguage = this.dataset.language;
      filterExamples();
      updateURL();
      updateActiveFilters();
    });
  });

  function filterExamples() {
    let visibleCount = 0;

    exampleCards.forEach(card => {
      const cardCategory = card.dataset.category || '';
      const cardLanguage = card.dataset.language || '';
      const cardTitle = (card.dataset.title || '').toLowerCase();
      const cardRepo = (card.dataset.repo || '').toLowerCase();
      const cardDescription = (card.dataset.description || '').toLowerCase();

      // Check category filter
      const categoryMatch = activeCategory === 'all' || cardCategory === activeCategory;

      // Check language filter
      const languageMatch = activeLanguage === 'all' || cardLanguage.includes(activeLanguage);

      // Check search query
      const searchMatch = searchQuery === '' ||
        cardTitle.includes(searchQuery) ||
        cardRepo.includes(searchQuery) ||
        cardDescription.includes(searchQuery);

      if (categoryMatch && languageMatch && searchMatch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // Update results count
    if (resultsCount) {
      resultsCount.textContent = `Showing ${visibleCount} of ${exampleCards.length} examples`;
    }

    // Show/hide no results message
    if (noResults) {
      noResults.style.display = visibleCount === 0 ? 'block' : 'none';
    }
  }

  // URL parameter management
  function initFromURL() {
    const params = new URLSearchParams(window.location.search);

    // Get category from URL
    const urlCategory = params.get('category');
    if (urlCategory) {
      activeCategory = urlCategory;
      categoryFilters.forEach(btn => {
        if (btn.dataset.category === urlCategory) {
          categoryFilters.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
      });
    }

    // Get language from URL
    const urlLanguage = params.get('language');
    if (urlLanguage) {
      activeLanguage = urlLanguage;
      languageFilters.forEach(btn => {
        if (btn.dataset.language === urlLanguage) {
          languageFilters.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        }
      });
    }

    // Get search from URL
    const urlSearch = params.get('search');
    if (urlSearch && searchInput) {
      searchQuery = urlSearch.toLowerCase();
      searchInput.value = urlSearch;
      updateClearButton();
    }

    // Apply filters
    filterExamples();
    updateActiveFilters();
  }

  function updateURL() {
    const params = new URLSearchParams();

    if (activeCategory !== 'all') {
      params.set('category', activeCategory);
    }
    if (activeLanguage !== 'all') {
      params.set('language', activeLanguage);
    }
    if (searchQuery) {
      params.set('search', searchQuery);
    }

    const newURL = params.toString()
      ? `${window.location.pathname}?${params.toString()}`
      : window.location.pathname;

    window.history.replaceState({}, '', newURL);
  }

  function updateClearButton() {
    if (searchClear) {
      if (searchQuery) {
        searchClear.classList.add('visible');
      } else {
        searchClear.classList.remove('visible');
      }
    }
  }

  function updateActiveFilters() {
    if (!activeFiltersContainer) return;

    activeFiltersContainer.innerHTML = '';

    if (activeCategory !== 'all') {
      const tag = createFilterTag('Category', formatCategoryName(activeCategory), () => {
        categoryFilters.forEach(btn => {
          btn.classList.remove('active');
          if (btn.dataset.category === 'all') {
            btn.classList.add('active');
          }
        });
        activeCategory = 'all';
        filterExamples();
        updateURL();
        updateActiveFilters();
      });
      activeFiltersContainer.appendChild(tag);
    }

    if (activeLanguage !== 'all') {
      const tag = createFilterTag('Language', capitalizeFirst(activeLanguage), () => {
        languageFilters.forEach(btn => {
          btn.classList.remove('active');
          if (btn.dataset.language === 'all') {
            btn.classList.add('active');
          }
        });
        activeLanguage = 'all';
        filterExamples();
        updateURL();
        updateActiveFilters();
      });
      activeFiltersContainer.appendChild(tag);
    }
  }

  function createFilterTag(label, value, onRemove) {
    const tag = document.createElement('span');
    tag.className = 'active-filter-tag';
    tag.innerHTML = `
      ${label}: ${value}
      <button aria-label="Remove ${label} filter">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    `;
    tag.querySelector('button').addEventListener('click', onRemove);
    return tag;
  }

  function formatCategoryName(category) {
    return category
      .split('-')
      .map(word => capitalizeFirst(word))
      .join(' ');
  }

  function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // Back to top functionality
  if (backToTop) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 400) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    }, { passive: true });

    backToTop.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }

      // If clicking a category link, also filter to that category
      const categoryMatch = href.match(/^#(complex-projects|developer-tooling|libraries-frameworks|infrastructure-projects|getting-started|project-handoffs)$/);
      if (categoryMatch) {
        const category = categoryMatch[1];
        categoryFilters.forEach(btn => {
          btn.classList.remove('active');
          if (btn.dataset.category === category) {
            btn.classList.add('active');
          }
        });
        activeCategory = category;
        filterExamples();
        updateURL();
        updateActiveFilters();
      }
    });
  });

  // Keyboard navigation for search
  if (searchInput) {
    document.addEventListener('keydown', function(e) {
      // Focus search on Cmd/Ctrl + K
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
      // Clear search on Escape
      if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        searchQuery = '';
        filterExamples();
        updateURL();
        updateClearButton();
        searchInput.blur();
      }
    });
  }

  // Handle browser back/forward navigation
  window.addEventListener('popstate', function() {
    initFromURL();
  });
});
