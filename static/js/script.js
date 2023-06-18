let show_all_btn = document.querySelector(".filter-all-btn");
let show_past_btn = document.querySelector(".filter-past-btn");
let show_ongoing_btn = document.querySelector(".filter-ongoing-btn");
let show_upcoming_btn = document.querySelector(".filter-upcoming-btn");

let show_all = document.querySelectorAll(".item");
let show_past = document.querySelectorAll(".filter-past");
let show_ongoing = document.querySelectorAll(".filter-ongoing");
let show_upcoming = document.querySelectorAll(".filter-upcoming");

let container = document.querySelector('.card-container');
let no_items_msg = document.querySelector('.no-items-msg');

var cards = document.querySelectorAll(".card");

[...cards].forEach((card) => {
  let learnMoreButton = card.querySelector(".learn-more-btn");
  let flipButton = card.querySelector(".flip-button");
  let cardFront = card.querySelector(".card-front");
  let cardBack = card.querySelector(".card-back");
  if (learnMoreButton) {
  learnMoreButton.addEventListener("click", function () {
    card.classList.toggle("card-flipped");
    if (card.classList.contains("card-flipped")) {
      cardFront.classList.add("d-none");
      cardBack.classList.remove("d-none");
    } else {
      cardFront.classList.remove("d-none");
      cardBack.classList.add("d-none");
    }
  })
};

  flipButton.addEventListener("click", function () {
    card.classList.toggle("card-flipped");
    if (card.classList.contains("card-flipped")) {
      cardFront.classList.add("d-none");
      cardBack.classList.remove("d-none");
    } else {
      cardFront.classList.remove("d-none");
      cardBack.classList.add("d-none");
    }
  });
});



show_past_btn.addEventListener("click", function () {
  toggleFilterButton(show_past_btn);
  showCards(show_past);
  hideCards(show_ongoing);
  hideCards(show_upcoming);
  toggleNoItemsMessage(no_items_msg);
});

show_ongoing_btn.addEventListener("click", function () {
  toggleFilterButton(show_ongoing_btn);
  showCards(show_ongoing);
  hideCards(show_past);
  hideCards(show_upcoming);
  toggleNoItemsMessage(no_items_msg);
});

show_upcoming_btn.addEventListener("click", function () {
  toggleFilterButton(show_upcoming_btn);
  showCards(show_upcoming);
  hideCards(show_past);
  hideCards(show_ongoing);
  toggleNoItemsMessage(no_items_msg);
});

show_all_btn.addEventListener("click", function () {
  toggleFilterButton(show_all_btn);
  showCards(show_all);
  toggleNoItemsMessage(no_items_msg);
});

function toggleFilterButton(clickedButton) {
  [show_all_btn, show_past_btn, show_ongoing_btn, show_upcoming_btn].forEach((button) => {
    if (button === clickedButton) {
      button.classList.add("filter-active");
    } else {
      button.classList.remove("filter-active");
    }
  });
}

function showCards(cards) {
  cards.forEach((card) => {
    card.classList.remove("d-none");
  });
}

function hideCards(cards) {
  cards.forEach((card) => {
    card.classList.add("d-none");
  });
}

function toggleNoItemsMessage() {
  let visibleCards = document.querySelectorAll(".item:not(.d-none)");
  if (visibleCards.length === 0) {
    no_items_msg.classList.remove("d-none");
  } else {
    no_items_msg.classList.add("d-none");
  }
}

toggleNoItemsMessage();
