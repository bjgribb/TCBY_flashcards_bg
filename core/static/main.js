
const slug = document.URL.split('/')[5]
const cardDataUrl = `/core/quiz/${slug}/get_card_data/`
const cardDisplay = query('.card-display')
const questionButton = query('.question-button')

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

// function that fetchs from URL
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
    cardDisplay.innerText = shuffledDeck[0][1]
    shuffledDeck.shift()
  })
}

function showQuestion (shuffledDeck) {
  questionButton.addEventListener('click', function () {
    if (shuffledDeck.length === 0) {
      cardDisplay.innerText = "You've finished!"
      questionButton.innerText = 'Done'
    } else {
      cardDisplay.innerText = shuffledDeck[0][0]
      questionButton.innerText = 'Next Question'
    }
  })
}

document.addEventListener('DOMContentLoaded', function () {
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
})
