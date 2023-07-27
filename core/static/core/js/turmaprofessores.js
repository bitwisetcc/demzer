var carousel3Swiper = new Swiper(".carousel3", {
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
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        },
        1280: {
            slidesPerView: 4,
        },
    },
});

function selectButton(index) {
  const contents = document.querySelectorAll('[id^="content-"]');
  const navItems = document.querySelectorAll('.nav-item');
  const indicator = document.getElementById('indicator');

  contents.forEach(content => {
    content.classList.add('hidden');
  });

  navItems.forEach(item => {
    item.classList.remove('selected');
  });

  const selectedContent = document.getElementById(`content-${index}`);
  selectedContent.classList.remove('hidden');
  
  const selectedItem = document.querySelector(`[onclick="selectButton(${index})"]`);
  selectedItem.classList.add('selected');

  // Atualiza a posição da barra de indicação
  indicator.style.transform = `translateX(${selectedItem.offsetLeft}px)`;
  indicator.style.width = `${selectedItem.offsetWidth}px`;
}
