var carousel2Swiper = new Swiper(".carousel2", {
      spaceBetween: 10,
      keyboard: {
        enabled: true,
      },
      navigation: {
        nextEl: ".carousel2 .swiper-button-next",
        prevEl: ".carousel2 .swiper-button-prev",
      },
      breakpoints:{
        768: {
            slidesPerView: 1,
        },
        1024: {
            slidesPerView: 1,
        },
        1280: {
            slidesPerView: 1,
        },
    },
});
