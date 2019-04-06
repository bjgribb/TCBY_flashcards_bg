// const cardData = '/core/get_cards/'
const Url = document.URL
const slug = Url.concat('/flashcards/')
const cardDisplay = query('.card-display')

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

document.addEventListener('DOMContentLoaded', function () {
  query('.card-display').addEventListener('click', function () {
    getDeckCards()
    getQuestionAnswer()
  })
})

function getDeckCards () {
  let promise = fetch('/core/quiz/roman-art/flashcards/').then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  return promise
}

function getQuestionAnswer () {
  getDeckCards('/core/quiz/roman-art/flashcards/')
    .then(cardData => {
      for (let card of Object.values((cardData))) {
        for (let data of card) {
          for (let question of data) {
            cardDisplay.innerText = question
          }
        }
      }
    })
}
