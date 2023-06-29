const requestURL = 'https://jsonplaceholder.typicode.com/users'

let inputIn = document.querySelector('.body-container__form__text');
let button = document.querySelector('.body-container__continue');

function sendRequest(method, url, body = null) {

	return new Promise( (resolve, reject) => {
		const xhr = new XMLHttpRequest()

		xhr.open(method, url)

		xhr.responseType = 'json'
		xhr.setRequestHeader('Content-Type', 'application/json')

		xhr.onload = () => {
			if (xhr.status >= 400){
				reject(xhr.response)
			}
			else {
				console.log(xhr.response)
			}
		}

		xhr.onerror = () => {
			reject(xhr.response)
		}

		xhr.send(JSON.stringify(body))

	} )

}

body = document.querySelector('.body-container__form__text');

button.onclick = function () {
	sendRequest('POST', requestURL, body)
		.then(data => console.log(data))
		.catch(err=>console.log(err))
}
