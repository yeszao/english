async function searchDictionary(offcanvasTitleEl, translationContentEl, word, to_lang) {
    translationContentEl.innerHTML = '';
    try {
        const response = await fetch(`/dictionary?to_lang=${to_lang}&text=${word}`);
        const data = await response.json();
        displayTranslation(offcanvasTitleEl, translationContentEl, data);
    } catch (error) {
        alert("Failed to fetch translation")
    }
}

function displayTranslation(offcanvasTitleEl, contentDiv, data) {
    offcanvasTitleEl.innerText = `${data.word}`;

    const pronunciationSection = document.createElement('div');
    data.pronunciations.forEach(pronunciation => {
        if (pronunciation.hasAudio) {
            const button = document.createElement('button');
            button.classList.add('btn', 'btn-outline-secondary', 'me-2', 'btn-sm', 'mb-2');
            button.innerHTML = `${pronunciation.accent} ${pronunciation.pronunciation} ၊၊||၊`;
            button.onclick = () => playAudio(pronunciation.id);
            pronunciationSection.appendChild(button);
        }
    });
    contentDiv.appendChild(pronunciationSection);

    // Group translations by posTag
    const groupedTranslations = data.translations.reduce((acc, { posTag, translation }) => {
        if (!acc[posTag]) {
            acc[posTag] = [];
        }
        acc[posTag].push(translation);
        return acc;
    }, {});

    // Render grouped translations
    Object.keys(groupedTranslations).forEach(posTag => {
        const groupSection = document.createElement('div');
        groupSection.innerHTML = `<p class="my-1"><span class="me-3 text-muted small">${posTag}.</span>${groupedTranslations[posTag].join(', ')}</p>`;
        contentDiv.appendChild(groupSection);
    });
}

function playAudio(pronunciationId) {
    // Assuming there's an API endpoint to fetch and play audio by pronunciation ID
    const audio = new Audio(`/play?id=${pronunciationId}`);
    audio.play();
}

function batchAction(inputList, action) {
    Array.from(inputList).forEach(item => action(item));
}

function initFontAndDarkButtons() {
    // Get stored values from localStorage
    let fontSize = localStorage.getItem('fontSize') || '16px';
    let darkMode = localStorage.getItem('darkMode') || 'light';

    // Apply initial values
    document.body.style.fontSize = fontSize;
    if (darkMode === 'dark') {
        document.body.classList.add('bg-dark', 'text-light');
    }

    // Button elements
    const decreaseFontBtn = document.getElementById('decreaseFont');
    const increaseFontBtn = document.getElementById('increaseFont');
    const toggleDarkModeBtn = document.getElementById('toggleDarkMode');

    // Decrease font size
    decreaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize - 1;
        document.body.style.fontSize = newSize + 'px';
        localStorage.setItem('fontSize', newSize + 'px');
    });

    // Increase font size
    increaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize + 1;
        document.body.style.fontSize = newSize + 'px';
        localStorage.setItem('fontSize', newSize + 'px');
    });

    // Toggle dark mode
    toggleDarkModeBtn.addEventListener('click', () => {
        document.body.classList.toggle('bg-dark');
        document.body.classList.toggle('text-light');
        darkMode = document.body.classList.contains('bg-dark') ? 'dark' : 'light';
        localStorage.setItem('darkMode', darkMode);
    });
}

function languageSelection() {
    const languageSelector = document.getElementById('language-selector');

    var currentLanguage = localStorage.getItem('language');
    if (currentLanguage) {
        languageSelector.value = currentLanguage;

        // set selected for the option
        var options = languageSelector.options;
        for (var i = 0; i < options.length; i++) {
            if (options[i].value === currentLanguage) {
                options[i].setAttribute('selected', 'selected');
            } else {
                options[i].removeAttribute('selected');
            }
        }
    }

    languageSelector.addEventListener('change', () => {
        localStorage.setItem('language', languageSelector.value);
    });
}

function saveReadingProgress(bookId, chapterNo, scrollPosition) {
    const readingProgress = {
        bookId: bookId,
        chapterNo: chapterNo,
        scrollPosition: scrollPosition,
    };
    localStorage.setItem('readingProgress', JSON.stringify(readingProgress));
}

// Track scroll position and save progress when the user scrolls or leaves the page
window.addEventListener('scroll', () => {
    saveReadingProgress(bookId, chapterNo, window.scrollY);
});

function loadReadingProgress() {
    const storedProgress = localStorage.getItem('readingProgress');

    if (storedProgress) {
        const { bookId, chapterNo, scrollPosition } = JSON.parse(storedProgress);
        console.log(`Resume reading Book ID: ${bookId}, Chapter: ${chapterNo}, Scroll Position: ${scrollPosition}`);

        // Logic to navigate to the saved chapter
        // Once in the correct chapter, scroll to the saved position
        window.scrollTo(0, scrollPosition);  // Scroll to the saved vertical position
    }
}

// Call this function on page load to restore the user's last position
window.addEventListener('load', loadReadingProgress);