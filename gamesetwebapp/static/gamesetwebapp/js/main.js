let currentPage = 1;

document.getElementById('next-button').addEventListener('click', () => {
    fetchGames(currentPage);
});

function fetchGames(page) {
    fetch(`/fetch-games?page=${page}`)
        .then(response => response.json())
        .then(data => {
            renderGames(data.games);
            currentPage = data.next_page; // Update the page for the next request
        })
        .catch(error => console.error('Error fetching games:', error));
}

function renderGames(games) {
    const gameList = document.getElementById('game-list');
    gameList.innerHTML = ''; // Clear the current list
    games.forEach(game => {
        const gameDiv = document.createElement('div');
        gameDiv.textContent = game.name; // Customize this to match your game data structure
        gameList.appendChild(gameDiv);
    });
}

// Initial fetch
fetchGames(currentPage);
