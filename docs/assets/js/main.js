// Search and Filter functionality for awesome-claude-md

document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const categoryFilters = document.querySelectorAll('.filter-btn[data-category]');
  const languageFilters = document.querySelectorAll('.filter-btn[data-language]');
  const exampleCards = document.querySelectorAll('.example-card');
  const resultsCount = document.getElementById('results-count');
  const noResults = document.getElementById('no-results');

  let activeCategory = 'all';
  let activeLanguage = 'all';
  let searchQuery = '';

  // Search functionality
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      searchQuery = e.target.value.toLowerCase().trim();
      filterExamples();
    });
  }

  // Category filter
  categoryFilters.forEach(btn => {
    btn.addEventListener('click', function() {
      categoryFilters.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      activeCategory = this.dataset.category;
      filterExamples();
    });
  });

  // Language filter
  languageFilters.forEach(btn => {
    btn.addEventListener('click', function() {
      languageFilters.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      activeLanguage = this.dataset.language;
      filterExamples();
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

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
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
      }
      // Clear search on Escape
      if (e.key === 'Escape' && document.activeElement === searchInput) {
        searchInput.value = '';
        searchQuery = '';
        filterExamples();
        searchInput.blur();
      }
    });
  }
});
