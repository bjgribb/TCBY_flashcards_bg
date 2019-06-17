const slug = document.URL.split('/')[5]
const cardDataUrl = `/home/quiz/${slug}/get_card_data/`
const scoreDisplay = query('.score-display')
const card = query('.card-main-container')
const cardFront = query('.card-front')
const cardBack = query('.card-back')
const startButton = query('.start-button')
let correctButton = query('.ask-if-correct')
let numCorrect = 0

function query (selector) {
  return document.querySelector(selector)
}

function queryAll (selector) {
  return document.querySelectorAll(selector)
}

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
  while (currentIndex !== 0) {
    randomIndex = Math.floor(Math.random() * currentIndex)
    currentIndex -= 1
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
      startGame(shuffledDeck)
      showQuestion(shuffledDeck)
      updateScore(numCorrect, shuffledDeck)
    })
}

function showQuestion (shuffledDeck) {
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('next')) {
      shuffledDeck.shift()
      if (shuffledDeck.length === 0) {
        cardFront.innerText = "You've finished!"
        cardBack.innerText = "You've finished!"
        startButton.innerHTML = ''
      } else {
        cardFront.innerText = shuffledDeck[0][0]
        cardBack.innerHTML = `<p>${shuffledDeck[0][1]}</p>
                              <i class="fas fa-check-circle ask-if-correct"></i>
                              <i class="fas fa-times-circle ask-if-wrong"></i>`
      }
    }
  })
}

function startGame (shuffledDeck) {
  startButton.addEventListener('click', function () {
    cardFront.innerText = shuffledDeck[0][0]
    cardBack.innerHTML = `<p>${shuffledDeck[0][1]}</p>
                          <i class="fas fa-check-circle ask-if-correct"></i>
                          <i class="fas fa-times-circle ask-if-wrong"></i>`
    startButton.innerHTML = `<i class="fas fa-arrow-circle-right next">
                            <p class='instructions'>NEXT</p></i>`
  })
}

function updateScore (numCorrect, shuffledDeck) {
  document.addEventListener('click', function (event) {
    if (event.target.classList.contains('ask-if-correct')) {
      numCorrect++
      scoreDisplay.innerText = numCorrect
      cardFront.innerHTML = `<p>${shuffledDeck[0][0]}</p>
                            <p class='instructions'>Click Next to view the next card</p>`
      cardBack.innerHTML = cardBack.innerHTML = `<p>${shuffledDeck[0][1]}</p>`
    } else {
      if (event.target.classList.contains('ask-if-wrong')) {
        cardFront.innerText = `<p>${shuffledDeck[0][0]}</p>
                              <p>Click Next to view the next card</p>`
        cardBack.innerHTML = cardBack.innerHTML = `<p>${shuffledDeck[0][1]}</p>`
      }
    }
  })
}

function flipCard () {
  if (card) {
    card.addEventListener('click', function () {
      card.classList.toggle('flip')
    })
  }
}

document.addEventListener('DOMContentLoaded', function () {
  flipCard()
  getDeckCards(cardDataUrl)
  getQuestionAnswer(cardDataUrl)
  updateScore(numCorrect)
})
