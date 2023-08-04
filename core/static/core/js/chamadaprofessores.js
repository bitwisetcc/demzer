const inputDate = document.getElementById('dataAtual');
const dataAtual = new Date().toISOString().split('T')[0];
inputDate.value = dataAtual;

//Table select

const quantidadeSelect = document.getElementById('quantidade');
const checkboxHeader = document.getElementById('checkbox-header');
const tableBody = document.getElementById('table-body');

// Define o valor padrão ao carregar a página
quantidadeSelect.value = '1';

quantidadeSelect.addEventListener('change', () => {
  const quantidade = parseInt(quantidadeSelect.value, 10);

  // Atualiza o cabeçalho das colunas
  checkboxHeader.colSpan = quantidade + 1;

  // Atualiza ou remove as colunas de checkbox nas linhas existentes
  const rows = tableBody.querySelectorAll('tr');
  rows.forEach(row => {
    const currentCheckboxes = row.querySelectorAll('td.checkbox-cell');
    const currentQuantidade = currentCheckboxes.length;

    if (currentQuantidade < quantidade) {
      for (let i = currentQuantidade; i < quantidade; i++) {
        const newCheckboxCell = document.createElement('td');
        newCheckboxCell.className = 'py-2 px-4 checkbox-cell';
        newCheckboxCell.innerHTML = '<input type="checkbox">';
        row.appendChild(newCheckboxCell);
      }
    } else if (currentQuantidade > quantidade) {
      for (let i = currentQuantidade; i > quantidade; i--) {
        row.removeChild(currentCheckboxes[i - 1]);
      }
    }
  });
});


