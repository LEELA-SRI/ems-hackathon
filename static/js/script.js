let show_all_btn=document.querySelector('.filter-all-btn')
let show_past_btn=document.querySelector('.filter-past-btn')
let show_ongoing_btn=document.querySelector('.filter-ongoing-btn')
let show_upcoming_btn=document.querySelector('.filter-upcoming-btn')
// console.log(show_all_btn,show_past_btn,show_ongoing_btn,show_upcoming_btn);

let show_all=document.querySelectorAll('.item')
let show_past=document.querySelectorAll('.filter-past')
let show_ongoing=document.querySelectorAll('.filter-ongoing')
let show_upcoming=document.querySelectorAll('.filter-upcoming')
// console.log(show_all,show_past,show_upcoming,show_ongoing);

show_past_btn.addEventListener('click',function(){
  show_past_btn.classList.add('filter-active')
  show_ongoing_btn.classList.remove('filter-active')
  show_upcoming_btn.classList.remove('filter-active')
  show_all_btn.classList.remove('filter-active')

  for (i of show_all){
    i.classList.add('d-none')
    // console.log(i);
  }
  for (i of show_past){
    i.classList.remove('d-none')
  }
})

show_ongoing_btn.addEventListener('click',function(){
  show_ongoing_btn.classList.add('filter-active')
  show_past_btn.classList.remove('filter-active')
  show_upcoming_btn.classList.remove('filter-active')
  show_all_btn.classList.remove('filter-active')
  for (i of show_all){
    i.classList.add('d-none')
    // console.log(i);
  }
  for (i of show_ongoing){
    i.classList.remove('d-none')
  }
})

show_upcoming_btn.addEventListener('click',function(){
  show_upcoming_btn.classList.add('filter-active')
  show_ongoing_btn.classList.remove('filter-active')
  show_past_btn.classList.remove('filter-active')
  show_all_btn.classList.remove('filter-active')

  for (i of show_all){
    i.classList.add('d-none')
    // console.log(i);
  }
  for (i of show_upcoming){
    i.classList.remove('d-none')
  }
})

show_all_btn.addEventListener('click',function(){
  show_all_btn.classList.add('filter-active')
  show_upcoming_btn.classList.remove('filter-active')
  show_ongoing_btn.classList.remove('filter-active')
  show_past_btn.classList.remove('filter-active')
  for (i of show_all){
    i.classList.remove('d-none')
    // console.log(i);
  }
  // for (i of show_upcoming){
  //   i.classList.remove('d-none')
  // }
})

var cards = document.querySelectorAll('.card');

[...cards].forEach((card)=>{
  card.addEventListener( 'click', function() {
    card.classList.toggle('card-flipped');
    if (card.classList.contains('card-flipped')){
      card.querySelector('.card-front').classList.add('d-none');
    card.querySelector('.card-back').classList.remove('d-none');

    }
    else{
      card.querySelector('.card-front').classList.remove('d-none');

    card.querySelector('.card-back').classList.add('d-none');
    }
    
  });
});