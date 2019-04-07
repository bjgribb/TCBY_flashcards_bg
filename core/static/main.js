
const slug = document.URL.split('/')[5]
const cardDataUrl = `/core/quiz/${slug}/get_card_data/`
const cardDisplay = query('.card-display')

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
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

// function getQuestionAnswer (cardDataUrl) {
//   getDeckCards(cardDataUrl)
//     .then(cardData => {
//       for (let card of Object.values(cardData)) {
//         query('.question-button').addEventListener('click', function () {
//           let idx = Math.floor(Math.random() * card.length)
//           cardDisplay.innerText = card[idx][0]
//           query('.answer-button').addEventListener('click', function () {
//             cardDisplay.innerText = card[idx][1]
//           })
//         })
//       }
//     })
// }

function getQuestionAnswer (cardDataUrl) {
  getDeckCards(cardDataUrl)
    .then(cardData => {
      for (let card of Object.values(cardData)) {
        query('.question-button').addEventListener('click', function () {
          let idx = Math.floor(Math.random() * card.length)
          cardDisplay.innerText = card[idx][0]
          query('.answer-button').addEventListener('click', function () {
            cardDisplay.innerText = card[idx][1]
          })
        })
      }
    })
}

document.addEventListener('DOMContentLoaded', function () {
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
})
