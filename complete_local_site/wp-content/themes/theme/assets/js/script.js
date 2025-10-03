$('.process-item').click(function () { 
 $('.process-item').removeClass('active');
 $(this).addClass('active');
 $('.process__content').removeClass('active');
 let id = $(this).attr('data-id') - 1;
 console.log(id)
 $('.process__content').eq(id).addClass('active');
});

$('.products-slider__item').click(function () { 
 $('.products-slider__item').removeClass('active');
 $(this).addClass('active');
 $('.products__item').removeClass('active');
 let id = $(this).attr('data-id') - 1;
 console.log(id)
 $('.products__item').eq(id).addClass('active');
});


let d = new Date();
let month = d.getMonth() + 1;

let day = d.getDate();
let output = day + '.' +  month + '.' +  d.getFullYear();

$('.download-price__circle p span').text(output);


$('.nav-item.home').prependTo('.nav');

let calcBannerTime = $('[calcBannerFixed_JS]').data('time') * 1000;
setTimeout(function () {
    $('[calcBannerFixed_JS]').addClass('visible');
}, calcBannerTime);