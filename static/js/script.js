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

  learnMoreButton.addEventListener("click", function () {
    card.classList.toggle("card-flipped");
    if (card.classList.contains("card-flipped")) {
      cardFront.classList.add("d-none");
      cardBack.classList.remove("d-none");
    } else {
      cardFront.classList.remove("d-none");
      cardBack.classList.add("d-none");
    }
  });

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
});

show_ongoing_btn.addEventListener("click", function () {
  toggleFilterButton(show_ongoing_btn);
  showCards(show_ongoing);
  hideCards(show_past);
  hideCards(show_upcoming);
});

show_upcoming_btn.addEventListener("click", function () {
  toggleFilterButton(show_upcoming_btn);
  showCards(show_upcoming);
  hideCards(show_past);
  hideCards(show_ongoing);
});

show_all_btn.addEventListener("click", function () {
  toggleFilterButton(show_all_btn);
  showCards(show_all);
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

// Initial state
toggleNoItemsMessage();

























// let show_all_btn = document.querySelector(".filter-all-btn");
// let show_past_btn = document.querySelector(".filter-past-btn");
// let show_ongoing_btn = document.querySelector(".filter-ongoing-btn");
// let show_upcoming_btn = document.querySelector(".filter-upcoming-btn");
// // console.log(show_all_btn,show_past_btn,show_ongoing_btn,show_upcoming_btn);

// let show_all = document.querySelectorAll(".item");
// let show_past = document.querySelectorAll(".filter-past");
// let show_ongoing = document.querySelectorAll(".filter-ongoing");
// let show_upcoming = document.querySelectorAll(".filter-upcoming");
// // console.log(show_all,show_past,show_upcoming,show_ongoing);

// let container = document.querySelector('.card-container');


// show_past_btn.addEventListener("click", function () {
//   show_past_btn.classList.add("filter-active");
//   show_ongoing_btn.classList.remove("filter-active");
//   show_upcoming_btn.classList.remove("filter-active");
//   show_all_btn.classList.remove("filter-active");

//   for (i of show_all) {
//     i.classList.add("d-none");
    
//   }
 
//   for (i of show_past) {
//     console.log(i);
//     i.classList.remove("d-none");
//   }
  
// });

// show_ongoing_btn.addEventListener("click", function () {
//   show_ongoing_btn.classList.add("filter-active");
//   show_past_btn.classList.remove("filter-active");
//   show_upcoming_btn.classList.remove("filter-active");
//   show_all_btn.classList.remove("filter-active");
//   for (i of show_all) {
//     i.classList.add("d-none");
   
//   }
//   if (show_ongoing.length != 0) {
//     for (i of show_ongoing){
//       console.log(i);
  
//       i.classList.remove('d-none')
//     }}
//     else{
//       console.log("none");
//     }
// });

// show_upcoming_btn.addEventListener("click", function () {
//   show_upcoming_btn.classList.add("filter-active");
//   show_ongoing_btn.classList.remove("filter-active");
//   show_past_btn.classList.remove("filter-active");
//   show_all_btn.classList.remove("filter-active");

//   for (i of show_all) {
//     i.classList.add("d-none");
    
//   }
//   if (show_upcoming.length != 0){
//   for (i of show_upcoming) {
//     i.classList.remove("d-none");
//   }}
//   else{
//     console.log("none")
//   }
// });

// show_all_btn.addEventListener("click", function () {
//   show_all_btn.classList.add("filter-active");
//   show_upcoming_btn.classList.remove("filter-active");
//   show_ongoing_btn.classList.remove("filter-active");
//   show_past_btn.classList.remove("filter-active");
//   if (show_all.length != 0){
//   for (i of show_all) {
//     i.classList.remove("d-none");
    
//   }}
//   else{
//     console.log('none');
//   }
 
// });

// var cards = document.querySelectorAll(".card");

// [...cards].forEach((card) => {
//   card.addEventListener("click", function () {
//     card.classList.toggle("card-flipped");
//     if (card.classList.contains("card-flipped")) {
//       card.querySelector(".card-front").classList.add("d-none");
//       card.querySelector(".card-back").classList.remove("d-none");
//     } else {
//       card.querySelector(".card-front").classList.remove("d-none");

//       card.querySelector(".card-back").classList.add("d-none");
//     }
//   });
// });
