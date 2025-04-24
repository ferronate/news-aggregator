document.addEventListener('DOMContentLoaded', () => {
    // Get the news feed container
    const newsFeed = document.getElementById('newsFeed');
    const newsCardTemplate = document.getElementById('newsCardTemplate');
    
    // Add a global variable to track current page
    let currentPage = 1;

    // Show loading state
    newsFeed.innerHTML = '<div class="loading">Loading news articles...</div>';
    
    // Fetch news data from API
    fetchNewsData();
    
    // Function to fetch news data from API
    async function fetchNewsData(page = 1) {
        try {
            const response = await fetch(`/api/news?page=${page}`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            renderNewsItems(data);
        } catch (error) {
            console.error('Error fetching news data:', error);
            newsFeed.innerHTML = `
                <div class="error-message">
                    <p>Failed to load news articles. Please try again later.</p>
                    <button id="retryButton">Retry</button>
                </div>
            `;
            
            document.getElementById('retryButton').addEventListener('click', () => fetchNewsData(page));
        }
    }
    
    // Function to render news items
    function renderNewsItems(items) {
        // Clear existing content
        newsFeed.innerHTML = '';
        
        if (!items || items.length === 0) {
            newsFeed.innerHTML = '<div class="error-message">No news articles found.</div>';
            return;
        }
        
        // Add each news item
        items.forEach(item => {
            const card = createNewsCard(item);
            newsFeed.appendChild(card);
        });
    }
    
    // Function to create a news card
    function createNewsCard(newsItem) {
        // Clone the template
        const cardElement = newsCardTemplate.content.cloneNode(true);
        const cardNode = cardElement.querySelector('.news-card');
        
        // Fill in the card data
        cardElement.querySelector('.news-title').textContent = newsItem.title;
        cardElement.querySelector('.news-author').textContent = 
            newsItem.author ? `By ${newsItem.author}` : 'Unknown author';
        
        // Use summary, content, or text depending on what's available
        const summaryElement = cardElement.querySelector('.news-summary');
        const fullSummary = newsItem.summary || newsItem.content || newsItem.text || '';
        summaryElement.textContent = fullSummary;
        
        // Check if summary needs truncation
        if (fullSummary.length > 150) {
            summaryElement.classList.add('truncated');
        }
        
        // Handle image if available
        const imageUrl = newsItem.image_url || newsItem.imageUrl || '';
        
        if (imageUrl) {
            // 1. Setup mini image for compact view
            const miniImageContainer = document.createElement('div');
            miniImageContainer.className = 'mini-image-container';
            
            const miniImage = document.createElement('img');
            miniImage.className = 'mini-image';
            miniImage.src = imageUrl;
            miniImage.alt = newsItem.title;
            miniImageContainer.appendChild(miniImage);
            
            // Add mini image to summary for small card view
            summaryElement.parentNode.insertBefore(miniImageContainer, summaryElement);
            
            // 2. Setup large image for expanded view
            const imageElement = cardElement.querySelector('.news-image');
            imageElement.src = imageUrl;
            imageElement.alt = newsItem.title;
            
            // Error handling for images
            imageElement.onerror = function() {
                const imageContainer = cardElement.querySelector('.card-image-container');
                imageContainer.style.display = 'none';
            };
            
            miniImage.onerror = function() {
                miniImageContainer.style.display = 'none';
            };
        } else {
            // No image URL provided - remove image containers
            const imageContainer = cardElement.querySelector('.card-image-container');
            imageContainer.style.display = 'none';
        }
        
        // Handle polarity slider
        const polarityThumb = cardElement.querySelector('.polarity-thumb');
        const polarityValue = cardElement.querySelector('.polarity-value');
        
        if (typeof newsItem.polarity !== 'undefined') {
            // Convert polarity (-1 to 1) to percentage (0% to 100%)
            const polarityPosition = ((parseFloat(newsItem.polarity) + 1) / 2) * 100;
            polarityThumb.style.left = `${polarityPosition}%`;
            updatePolarityValue(newsItem.polarity, polarityValue);
        }
        
        // Handle subjectivity slider
        const subjectivityThumb = cardElement.querySelector('.subjectivity-thumb');
        const subjectivityValue = cardElement.querySelector('.subjectivity-value');
        
        if (typeof newsItem.subjectivity !== 'undefined') {
            // Convert subjectivity (0 to 1) to percentage (0% to 100%)
            const subjectivityPosition = parseFloat(newsItem.subjectivity) * 100;
            subjectivityThumb.style.left = `${subjectivityPosition}%`;
            updateSubjectivityValue(newsItem.subjectivity, subjectivityValue);
        }
        
        // Create expanded content section
        const expandContent = document.createElement('div');
        expandContent.className = 'expand-content';
        
        // Create article URL button
        const articleUrl = document.createElement('a');
        articleUrl.href = newsItem.url;
        articleUrl.className = 'article-url';
        articleUrl.textContent = 'Read Full Article';
        articleUrl.target = '_blank';
        expandContent.appendChild(articleUrl);
        
        // Add expanded content to card
        cardElement.querySelector('.card-content').appendChild(expandContent);
        
        // Add event listener for card interaction
        cardNode.addEventListener('click', function(event) {
            this.classList.toggle('expanded');
            
            // Prevent click propagation to document click handler
            event.stopPropagation();
        });
        
        return cardElement;
    }
    
    // Add global document click listener to collapse cards when clicking elsewhere
    document.addEventListener('click', function() {
        const expandedCards = document.querySelectorAll('.news-card.expanded');
        expandedCards.forEach(card => {
            card.classList.remove('expanded');
        });
    });
    
    // Update polarity display
    function updatePolarityValue(value, element) {
        let text, color;
        value = parseFloat(value);
        
        if (value > 0.75) {
            text = 'Extremely positive';
            color = 'var(--positive-color)';
        } else if (value > 0.5) {
            text = 'Significantly positive';
            color = 'var(--positive-color)';
        } else if (value > 0.3) {
            text = 'Fairly positive';
            color = 'var(--positive-color)';
        } else if (value > 0.1) {
            text = 'Slightly positive';
            color = 'var(--positive-color)';
        } else if (value < -0.75) {
            text = 'Extremely negative';
            color = 'var(--negative-color)';
        } else if (value < -0.5) {
            text = 'Significantly negative';
            color = 'var(--negative-color)';
        } else if (value < -0.3) {
            text = 'Fairly negative';
            color = 'var(--negative-color)';
        } else if (value < -0.1) {
            text = 'Slightly negative';
            color = 'var(--negative-color)';
        } else {
            text = 'Neutral';
            color = 'var(--neutral-color)';
        }
        
        element.textContent = text;
        element.style.backgroundColor = color;
    }
    
    // Update subjectivity display
    function updateSubjectivityValue(value, element) {
        let text, color;
        value = parseFloat(value);
        
        if (value > 0.75) {
            text = 'Extremely subjective';
            color = 'var(--subjective-color)';
        } else if (value > 0.5) {
            text = 'Fairly subjective';
            color = 'var(--subjective-color)';
        } else if (value > 0.3) {
            text = 'Fairly objective';
            color = 'var(--objective-color)';
        } else if (value > 0.1) {
            text = 'Extremely objective';
            color = 'var(--objective-color)';
        } else {
            text = 'Extremely objective';
            color = 'var(--objective-color)';
        }
        
        element.textContent = text;
        element.style.backgroundColor = color;
    }
    
    // Search functionality
    const searchBox = document.querySelector('.search-box input');
    const searchButton = document.querySelector('.search-box button');
    
    searchButton.addEventListener('click', performSearch);
    searchBox.addEventListener('keypress', event => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
    
    function performSearch() {
        const searchTerm = searchBox.value.trim().toLowerCase();
        if (searchTerm === '') return;
        
        // Show loading state
        newsFeed.innerHTML = '<div class="loading">Searching articles...</div>';
        
        // For client-side search, get all articles first
        fetch('/api/news')
            .then(response => response.json())
            .then(data => {
                const filteredArticles = data.filter(article => 
                    article.title.toLowerCase().includes(searchTerm) || 
                    (article.summary && article.summary.toLowerCase().includes(searchTerm)) ||
                    (article.author && article.author.toLowerCase().includes(searchTerm))
                );
                
                renderNewsItems(filteredArticles);
            })
            .catch(error => {
                console.error('Error during search:', error);
                newsFeed.innerHTML = '<div class="error-message">Error searching articles.</div>';
            });
    }

    // Dark mode functionality
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    if (darkModeToggle) {
        // Check for saved preference
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
        darkModeToggle.checked = savedTheme === 'dark';
        
        // Listen for toggle changes
        darkModeToggle.addEventListener('change', () => {
            if (darkModeToggle.checked) {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Refresh button functionality
    const refreshButton = document.getElementById('refreshButton');
    if (refreshButton) {
        refreshButton.addEventListener('click', async function() {
            this.classList.add('rotating');
            
            try {
                // Toggle between page 1 and 2
                currentPage = currentPage === 1 ? 2 : 1;
                
                // Show loading state
                newsFeed.innerHTML = '<div class="loading">Refreshing news articles...</div>';
                
                // Fetch the newly toggled page
                await fetchNewsData(currentPage);
                
                // Start background refresh if we're showing page 1 again
                if (currentPage === 1) {
                    await fetch('/api/refresh', {
                        method: 'POST'
                    });
                }
            } catch (error) {
                console.error('Error refreshing news:', error);
                newsFeed.innerHTML = '<div class="error-message">Error refreshing news</div>';
            } finally {
                // Stop rotation after a delay to make it look smooth
                setTimeout(() => {
                    this.classList.remove('rotating');
                }, 1000);
            }
        });
    }
});