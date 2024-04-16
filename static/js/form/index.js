'use strict';

let currentState = 1;

window.onload = function(){
  const form = document.querySelector('.form');
  form.addEventListener('submit', function(event) {
    event.preventDefault()
  })

  function setClassForStep(list, itemId, className) {
    list.forEach(function(item) {
      if(item.dataset.step == itemId) {
        item.classList.add(className);
      } else {
        item.classList.remove(className);
      }
    });
  }

  function setClassForStepIndicator(list, itemId, className) {
    list.forEach(function(item) {
      if(item.dataset.step == itemId || item.dataset.step < itemId) {
        item.classList.add(className);
      } else {
        item.classList.remove(className);
      }
    });
  }

  function changeFormState() {
    const backButton = document.querySelector('.form-buttons__back'),
      nextButton = document.querySelector('.form-buttons__next');

    const steps = document.querySelectorAll('.form__step'),
      progressListItems = document.querySelectorAll('.progress-list__item');

      // setClassForStep(steps, currentState, 'current');
      // setClassForStepIndicator(progressListItems, currentState, 'done')

    nextButton.addEventListener('click', function() {
      if (currentState < 7) {
        ++currentState;
        setClassForStep(steps, currentState, 'current');
        setClassForStepIndicator(progressListItems, currentState, 'done')
      }
    });

    backButton.addEventListener('click', function() {
      if (--currentState > 0) {
        setClassForStep(steps, currentState, 'current');
        setClassForStepIndicator(progressListItems, currentState, 'done')
      }
    });
  }

  changeFormState();
}