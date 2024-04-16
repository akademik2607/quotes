'use strict';

$(function(){
const result = document.querySelector('.calc-content__result');
result.value = 0;

  $('.calc-content-item__minus').on('click', function(event){
    let parent = event.target.closest('.calc-content__item');
    console.log(parent);

    const voluemItem = parent.querySelector('.calc-content-item__volume'),
      countItem = parent.querySelector('.calc-conten-item__input');

    let voluem = parseFloat(voluemItem.dataset.value),
      count = parseInt(countItem.dataset.value),
      resultNum = parseFloat(result.value);

    console.log(countItem.dataset);
    resultNum -= voluem * count;
    --count;
    resultNum += voluem * count;

    result.value = resultNum;
    countItem.innerHTML = count;
    countItem.dataset.value = count;

  })


  $('.calc-content-item__plus').on('click', function(event){
    let parent = event.target.closest('.calc-content__item');
    console.log(parent);

    const voluemItem = parent.querySelector('.calc-content-item__volume'),
      countItem = parent.querySelector('.calc-conten-item__input');

    let voluem = parseFloat(voluemItem.dataset.value),
      count = parseInt(countItem.dataset.value),
      resultNum = parseFloat(result.value);

    console.log(countItem.dataset);
    resultNum -= voluem * count;
    ++count;
    resultNum += voluem * count;

    resultNum = resultNum.toFixed(2)
    result.value = resultNum;
    countItem.innerHTML = count;
    countItem.dataset.value = count;

  })

});