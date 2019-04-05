const cardData = 'get_cards/'

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

query('.card-display').addEventListener('click', function () {
  getCards(cardData)
})

function getCards (cardData) {
  let promise = fetch(cardData).then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  console.log(promise)
  return promise
}
