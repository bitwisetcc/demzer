var carousel1Swiper = new Swiper(".carousel1", {
  slidesPerView: 1,
  keyboard: {
    enabled: false,
  },
  navigation: {
    nextEl: ".carousel1 .swiper-button-next",
    prevEl: ".carousel1 .swiper-button-prev",
  },
});

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
        360: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
        1280: {
            slidesPerView: 4,
        },
        1536: {
            slidesPerView: 5,
      },
    },
});
