const inputDate = document.getElementById('dataAtual');
const dataAtual = new Date().toISOString().split('T')[0];
inputDate.value = dataAtual;

