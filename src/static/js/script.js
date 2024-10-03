async function searchDictionary(offcanvasTitleEl, offcanvasContentEl, word, to_lang) {
    try {
        const response = await fetch(`/dictionary?to_lang=${to_lang}&text=${word}`);
        const data = await response.json();
        displayTranslation(offcanvasTitleEl, offcanvasContentEl, data);
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

function saveReadingProgress(bookSlug, chapterNo, sentenceId) {
    const readingProgress = {
        chapterNo: chapterNo,
        sentenceId: sentenceId,
    };
    localStorage.setItem(`bookReadingProgress_${bookSlug}`, JSON.stringify(readingProgress));
}

function getReadingProgress(bookSlug) {
    return localStorage.getItem(`bookReadingProgress_${bookSlug}`);
}

function loadReadingProgressToButton(buttonSelector) {
    var readButtonEls = document.querySelectorAll(buttonSelector);
    Array.from(readButtonEls).forEach(buttonEl => {
        const bookSlug = buttonEl.dataset.bookSlug;
        const storedProgress = getReadingProgress(bookSlug);
        console.log(storedProgress);

        if (storedProgress) {
            const { chapterNo, sentenceId } = JSON.parse(storedProgress);
            buttonEl.href = `/book/${bookSlug}/chapter-${chapterNo}.html#${sentenceId}`;
            buttonEl.innerText = `Continue from chapter ${chapterNo} sentence ${sentenceId}`;
        }
    });
}

function getFirstVisibleSentenceId() {
    // Get all <s> tags on the page
    const sTags = document.querySelectorAll('s');

    // Loop through the <s> tags to find the first visible one
    for (let sTag of sTags) {
        const rect = sTag.getBoundingClientRect();

        // Check if the element is in the visible window (partially or fully)
        if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
            // Return the id of the first visible <s> tag
            return sTag.id;
        }
    }

    return 1;
}