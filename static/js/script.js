
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


async function fetchTranslation(word) {
    try {
        // Assuming you have an API endpoint that provides the translation
        const response = await fetch(`/translate?from_lang=en&to_lang=zh-Hans&text=${word}`);
        const data = await response.json();
        displayTranslation(data);
    } catch (error) {
        console.error('Error fetching translation:', error);
    }
}

function displayTranslation(data) {
    const contentDiv = document.getElementById('translationContent');
    contentDiv.innerHTML = '';

    // Word and pronunciation section
    const wordSection = document.createElement('div');
    wordSection.innerHTML = `<h3>${data.word}</h3>`;

    const pronunciationSection = document.createElement('div');
    pronunciationSection.innerHTML = `
    <button class="btn btn-secondary" onclick="playAudio('${data.pronunciations.find(p => p.accent === 'UK').id}')">UK Voice</button>
    <button class="btn btn-secondary" onclick="playAudio('${data.pronunciations.find(p => p.accent === 'US').id}')">US Voice</button>
  `;

    contentDiv.appendChild(wordSection);
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
        groupSection.innerHTML = `<h5>${posTag}</h5><p>${groupedTranslations[posTag].join(', ')}</p>`;
        contentDiv.appendChild(groupSection);
    });
}

function playAudio(pronunciationId) {
    // Assuming there's an API endpoint to fetch and play audio by pronunciation ID
    const audio = new Audio(`/play?id=${pronunciationId}`);
    audio.play();
}
