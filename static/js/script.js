
var captureWordOnClick = function(containerEl, callback) {
    containerEl.addEventListener('click', function (event) {
        // Get the mouse position relative to the clicked element
        const x = event.clientX;
        const y = event.clientY;

        // Get caret position at the point of click
        const caretPosition = document.caretPositionFromPoint(x, y);

        // If the click is on text, the offsetNode should be a text node
        if (caretPosition && caretPosition.offsetNode.nodeType === Node.TEXT_NODE) {
            // Get the full text where the click happened
            const fullText = caretPosition.offsetNode.nodeValue;

            // Get the clicked word by splitting text around the clicked character
            const offset = caretPosition.offset;
            const words = fullText.split(' ');

            // Find which word was clicked by checking the offsets
            let charCount = 0;
            for (let word of words) {
                if (offset <= charCount + word.length) {
                    // Clean the word by removing punctuation at the end
                    const cleanedWord = word.replace(/[.,!?;:"]+$/, '');
                    callback(cleanedWord);
                    break;
                }
                charCount += word.length + 1; // +1 for spaces
            }
        }
    });
};


async function fetchTranslation(offcanvasTitleEl, translationContentEl,  word) {
    translationContentEl.innerHTML = '';
    try {
        // Assuming you have an API endpoint that provides the translation
        const response = await fetch(`/translate?from_lang=en&to_lang=zh-Hans&text=${word}`);
        const data = await response.json();
        displayTranslation(offcanvasTitleEl, translationContentEl, data);
    } catch (error) {
        console.error('Error fetching translation:', error);
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
