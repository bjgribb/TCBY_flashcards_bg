
// const drake = require('dragula')
// const justFlipIt = require('justflipit')

const slug = document.URL.split('/')[5]
const cardDataUrl = `/core/quiz/${slug}/get_card_data/`
const cardDisplay = query('.card-display')
const questionButton = query('.question-button')
const scoreDisplay = query('.score-display')
const cardFront = query('.card-front')
const cardBack = query('.card-back')
const answerButton = query('.answer-button')
let correctButton = query('.ask-if-correct')
let incorrectButton = query('.ask-if-wrong')
let numCorrect = 0

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

// function that fetchs from URL
function hideButtons (button) {
  button.hidden = true
}

function showButtons (button) {
  button.hidden = false
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

// courtesy https://gomakethings.com/how-to-shuffle-an-array-with-vanilla-js/ - shuffles deck on refresh
function shuffle (array) {
  var currentIndex = array.length
  var temporaryValue, randomIndex
  // While there remain elements to shuffle...
  while (currentIndex !== 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex -= 1
    // And swap it with the current element.
    temporaryValue = array[currentIndex]
    array[currentIndex] = array[randomIndex]
    array[randomIndex] = temporaryValue
  }
  return array
}

function getQuestionAnswer (cardDataUrl) {
  getDeckCards(cardDataUrl)
    .then(cardData => {
      let array = (Object.values(cardData)[0])
      let shuffledDeck = (shuffle(array))
      const totalDeck = shuffledDeck.length
      showQuestion(shuffledDeck)
      showAnswer(shuffledDeck)
      updateScore(numCorrect, shuffledDeck, totalDeck)
    })
}

function showAnswer (shuffledDeck) {
  query('.answer-button').addEventListener('click', function () {
    showButtons(correctButton)
    showButtons(incorrectButton)
    hideButtons(questionButton)
    hideButtons(answerButton)
    cardBack.innerText = shuffledDeck[0][1]
    shuffledDeck.shift()
  })
}

function showQuestion (shuffledDeck) {
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('ask-if-correct') ||
    (event.target.classList.contains('ask-if-wrong') ||
    (event.target.classList.contains('question-button')))) {
      hideButtons(correctButton)
      hideButtons(incorrectButton)
      showButtons(answerButton)
      cardBack.innerText = ' '
      if (shuffledDeck.length === 0) {
        cardFront.innerText = "You've finished!"
        hideButtons(questionButton)
        hideButtons(answerButton)
      } else {
        cardFront.innerText = shuffledDeck[0][0]
        hideButtons(questionButton)
      }
    }
  })
}

function updateScore (numCorrect, shuffledDeck, totalDeck) {
  correctButton.addEventListener('click', function () {
    numCorrect++
    scoreDisplay.innerText = numCorrect
    if (shuffledDeck.length < 1) {
      scoreDisplay.innerText = `${numCorrect} out of ${totalDeck}`
    }
  })
}

// document.addEventListener('click', function (event) {
//   if (event.target.classList.contains('ask-if-correct') ||
//   (event.target.classList.contains('ask-if-wrong'))) {
//     hideButtons(correctButton)
//     hideButtons(incorrectButton)
//     showButtons(answerButton)
//     cardBack.innerText = ' '
//     if (shuffledDeck.length === 0) {
//       cardFront.innerText = "You've finished!"
//       hideButtons(questionButton)
//     } else {
//       cardFront.innerText = shuffledDeck[0][0]
//       questionButton.innerText = 'Next Question'
//     }
//   }
// })

document.addEventListener('DOMContentLoaded', function () {
  hideButtons(correctButton)
  hideButtons(incorrectButton)
  hideButtons(answerButton)
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
  // updateScore(numCorrect)
})
