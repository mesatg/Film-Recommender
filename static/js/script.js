const searchInput = document.getElementById('movie-input');
const suggestionsBox = document.getElementById('suggestions');
const selectedMovieDiv = document.getElementById('selected-movie');
const recommendBtn = document.getElementById('recommend-btn');
const recBox = document.getElementById('recommendations');

// ✅ Boş eleman kontrolü
if (!searchInput || !suggestionsBox || !selectedMovieDiv || !recommendBtn || !recBox) {
    console.error('⚠️ Gerekli HTML elemanları bulunamadı!');
}

// ✅ Otomatik Doldurma İşlevi
searchInput.addEventListener('input', async () => {
    const query = searchInput.value.trim();
    if (query.length > 0) {
        try {
            const response = await fetch(`/autocomplete?query=${encodeURIComponent(query)}`);
            const suggestions = await response.json();
            suggestionsBox.innerHTML = '';
            suggestions.forEach(movie => {
                const div = document.createElement('div');
                div.textContent = movie;
                div.classList.add('suggestion');
                div.style.cursor = 'pointer';
                div.addEventListener('click', () => {
                    searchInput.value = movie;
                    suggestionsBox.innerHTML = '';
                });
                suggestionsBox.appendChild(div);
            });
        } catch (error) {
            console.error('🚨 Otomatik tamamlama hatası:', error);
        }
    } else {
        suggestionsBox.innerHTML = '';
    }
});

// ✅ Önerilen Filmleri ve Seçilen Filmin Posterini Getir
async function recommend() {
    const movieName = searchInput.value.trim();
    if (!movieName) {
        console.warn('⚠️ Film ismi boş.');
        return;
    }

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ movie: movieName })
        });

        const data = await response.json();
        console.log('📦 Gelen Yanıt:', data);

        if (!recBox || !selectedMovieDiv) return;
        selectedMovieDiv.innerHTML = '';
        recBox.innerHTML = '';

        if (data.main_poster) {
            const img = document.createElement('img');
            img.src = data.main_poster;
            img.alt = movieName;
            img.style.width = '100px';
            img.style.borderRadius = '10px';
            selectedMovieDiv.appendChild(img);
        }

        if (data.recommended && data.recommended.length > 0) {
            data.recommended.forEach(movie => {
                const movieDiv = document.createElement('div');
                movieDiv.classList.add('movie-item');

                const img = document.createElement('img');
                img.src = movie.poster || '/static/images/default_poster.png';
                img.alt = movie.title;
                img.style.width = '150px';
                img.style.borderRadius = '10px';

                const title = document.createElement('p');
                title.textContent = movie.title;

                movieDiv.appendChild(img);
                movieDiv.appendChild(title);
                recBox.appendChild(movieDiv);
            });
        } else {
            recBox.innerHTML = `<li>⚠️ ${data.error || 'Öneri bulunamadı.'}</li>`;
        }
    } catch (error) {
        console.error('🚨 Öneri getirilirken hata oluştu:', error);
    }
}

recommendBtn.addEventListener('click', recommend);