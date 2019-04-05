const cardData = '/core/get_cards/'

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

document.addEventListener('DOMContentLoaded', function () {
  query('.card-display').addEventListener('click', function () {
    console.log('hello')
    getCards()
  })
})

function getCards () {
  let promise = fetch('/core/get_cards/').then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  console.log(promise)
  return promise
}
