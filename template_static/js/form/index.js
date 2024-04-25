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
        console.log(steps)
        console.log(currentState);
        setClassForStep(steps, currentState, 'current');
        setClassForStepIndicator(progressListItems, currentState, 'done')
      } else {
        const userId = document.querySelector('input[name="user_id"]').value,
          service = document.querySelector('#service').value,
          moveDate = document.querySelector('input[name="move-date"]').value,
          needStorage = document.querySelector('input[name="need-storage"]').value,
          fromCountry = document.querySelector('#from-country').value,
          fromCity = document.querySelector('#from-city').value,
          fromAddress = document.querySelector('#from-address').value,
          fromMethod = document.querySelector('#from-method').value,
          toCountry = document.querySelector('#to-country').value,
          toCity = document.querySelector('#to-city').value;

          const whatList = document.querySelectorAll('input[name="what"]');
          const what = [];
          whatList.forEach((item) => {
            if(item.checked)
            what.push(item.value)
          });
          // .filter((item) => item.checked).map((item) => item.value);

          const calcCesult = document.querySelector('input[name="calc-result"]').value,
          isAssemblyList = document.querySelectorAll('input[name="is_assembly"]'),
          isAssembly = [];
          isAssemblyList.forEach((item) => {
            if(item.checked)
            isAssembly.push(item.value)
          });
         
          const havePianoList = document.querySelectorAll('input[name="have_piano"]'),
            have_Piano = [];
          havePianoList.forEach((item) => {
            if(item.checked)
            have_Piano.push(item.value)
          });
          
          const howManyPeopleList = document.querySelectorAll('input[name="how_many_people"]'),
            howManyPeople = [];
          howManyPeopleList.forEach((item) => {
            if(item.checked)
            howManyPeople.push(item.value)
          });
          // needInsurance = document.querySelectorAll('input[name="how_many_people"]').filter((item) => item.checked).map((item) => item.value),
          const needInsurance = 'Yes',
          insuranceValue = 345,

          firstName = document.querySelector('#pers-firstname').value,
          lastName = document.querySelector('#pers-lastname').value,
          email = document.querySelector('#pers-email').value,
          phone = document.querySelector('#pers-phone').value,
          isPrivate = 'Yes';

          $.ajax(
            
            'https://hook.eu1.make.com/l2le7lsb6dv1g92edtmsh2ff6lwigct2',
            {
              method: 'post',
              data: {
                'user_id': userId,
                'service': service,
                'move_date': moveDate,
                'need_storage': needStorage,
                'from_country':fromCountry,
                'from_city': fromCity,
                'from_address': fromAddress,
                'from_method': fromMethod,
                'to_country': fromMethod,
                'toCity': fromMethod,
                'what':what,
                'calcCesult': calcCesult,
                'isAssembly':isAssembly,
                'have_piano': have_Piano,
                'howManyPeople': howManyPeople,
            // needInsurance = document.querySelectorAll('input[name="how_many_people"]').filter((item) => item.checked).map((item) => item.value),
                'needInsurance': howManyPeople,
                'insuranceValue':insuranceValue,
  
            'firstName': firstName,
            'lastName': lastName,
            'email':email,
            'phone':phone,
            
            'isPrivate': isPrivate
              }
            
            ,
            success: function(responce) {
              console.log(responce);
            }
          }
          )

          // user_id
            // service
            // move-date
            // need-storage
            // from-country
            // from-city
            // from-address
            // from-method
            // to-country
            // to-city
            // what
            // calc-result
            // is_assembly
            // have_piano
            // how_many_people
            // need_insurance
            // insurance_value
            // first_name
            // last_name
            // email
            // phone
            // is_private
            // anything
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