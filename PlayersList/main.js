async function getResponse() 
{
    let response = await fetch('https://jsonplaceholder.typicode.com/users')
    let content = await response.json()
    content = content.splice(0, 5)
    console.log(content)

    let list = document.querySelector('.players')



    let key
    for (key in content)
    {
        list.innerHTML += `
        <div class="player1 divv">
        <div class="left">
           <img class ="person" src="person.svg"> 
           <div class ="name1">
           ${content[key].name}
           </div>
        </div>
        <div class="right">
           <button class="button1" onclick="document.location='Folder/Offer.html'"> <img class ="offer" src="offer.svg", width= 20px> 
           </button>
           <button class="button1" onclick="document.location='Folder/Accept.html'"> <img class ="accept" src="accept.svg", width= 20px> 
           </button>
        </div>
        
        </div>
        `
    }
}

getResponse()