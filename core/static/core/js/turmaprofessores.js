const inputDate = document.getElementById('dataAtual');
const dataAtual = new Date().toISOString().split('T')[0];
inputDate.value = dataAtual;

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
