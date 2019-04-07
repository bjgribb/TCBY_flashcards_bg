
const slug = document.URL.split('/')[5]
const cardDataUrl = `/core/quiz/${slug}/get_card_data/`
const cardDisplay = query('.card-display')
const questionButton = query('.question-button')
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

// function that fetchs from URL
function hideButtons (button) {
  button.hidden = true
  console.log('correcthide')
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
      showQuestion(shuffledDeck)
      showAnswer(shuffledDeck)
    })
}

function showAnswer (shuffledDeck) {
  query('.answer-button').addEventListener('click', function () {
    showButtons(correctButton)
    showButtons(incorrectButton)
    cardBack.innerText = shuffledDeck[0][1]
    shuffledDeck.shift()
  })
}

function showQuestion (shuffledDeck) {
  questionButton.addEventListener('click', function () {
    hideButtons(correctButton)
    hideButtons(incorrectButton)
    cardBack.innerText = ' '
    if (shuffledDeck.length === 0) {
      cardFront.innerText = "You've finished!"
      questionButton.innerText = 'Done'
    } else {
      cardFront.innerText = shuffledDeck[0][0]
      questionButton.innerText = 'Next Question'
    }
  })
}

// function tallyCorrect () {
//   let score = 0
// }

document.addEventListener('DOMContentLoaded', function () {
  hideButtons(correctButton)
  hideButtons(incorrectButton)
  // hideButtons(cardBack)
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
})
