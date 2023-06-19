let playersAmount = document.getElementById('playersAmount');

function getPlayersAmount() {
    fetch("https://jsonplaceholder.typicode.com/users")
    .then(response => response.json())
    .then(data => {
		playersAmount.textContent = data.length;
    })
    .catch(error => {
        console.log("Error:", error);
    });
}

getPlayersAmount();