
const slug = document.URL.split('/')[5]
const cardDataUrl = `/core/quiz/${slug}/get_card_data/`
const cardDisplay = query('.card-display')
const cardFront = query('.card-front')
const cardBack = query('.card-back')
let correctButton = query('.ask-if-correct')
let incorrectButton = query('.ask-if-wrong')

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

function hideButtons () {
  correctButton.hidden = true
  incorrectButton.hidden = true
  console.log('correcthide')
}

function showButtons () {
  correctButton.hidden = false
  incorrectButton.hidden = false
}

function getDeckCards (cardDataUrl) {
  let promise = fetch(cardDataUrl).then(function (response) {
    if (!response.ok) {
      throw Error(response.statusText)
    }
    return response.json()
  })
  return promise
}

function getQuestionAnswer (cardDataUrl) {
  getDeckCards(cardDataUrl)
    .then(cardData => {
      for (let card of Object.values(cardData)) {
        query('.question-button').addEventListener('click', function () {
          let idx = Math.floor(Math.random() * card.length)
          cardFront.innerText = card[idx][0]
          query('.answer-button').addEventListener('click', function () {
            c
            cardBack.innerText = card[idx][1]
          })
        })
      }
    })
}

// function tallyCorrect () {
//   let score = 0
// }

document.addEventListener('DOMContentLoaded', function () {
  hideButtons()
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
})
