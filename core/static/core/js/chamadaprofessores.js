//Tabela

function atualizarTabela() {
  const quantidadeAulas = parseInt(document.getElementById("quantidadeAulas").value);
  const tabela = document.querySelector("table");
  const cabecalho = tabela.querySelector("thead tr");
  const corpo = tabela.querySelector("tbody");

  // Limpa a tabela existente
  cabecalho.innerHTML = "<th class='border px-4 py-2'>Nome do Aluno</th>";
  corpo.innerHTML = "";

  // Adiciona colunas de aulas ao cabeçalho
  for (let i = 1; i <= quantidadeAulas; i++) {
    cabecalho.innerHTML += `<th class='border px-4 py-2'>${i}</th>`;
  }

  // Adiciona linhas de alunos com checkboxes de faltas
  const alunos = ["João Santana Silva Moderato", "Maria", "Giovanni de Pita Cicero", "João Santana Silva Merato", "Maria", "Giovanni de Pita Cicero", "João Santana Silva Moderato", "Maria", "Giovanni de Pita Cicero"]; // Substitua pelos nomes dos alunos reais
  for (const aluno of alunos) {
    let newRow = document.createElement("tr");
    let newCell = document.createElement("td");
    newCell.classList.add("border", "px-4", "py-2", "text-center");
    newCell.textContent = aluno;
    newRow.appendChild(newCell);

    for (let i = 0; i < quantidadeAulas; i++) {
      newCell = document.createElement("td");
      newCell.classList.add("border", "px-4", "py-2", "text-center");
      newCell.innerHTML = `<input type="checkbox" class="form-checkbox h-6 w-6 rounded-full text-red-500 focus:ring focus:ring-red-300">`;
      newRow.appendChild(newCell);
    }

    corpo.appendChild(newRow);
  }
}

// Chama a função inicialmente e sempre que a quantidade de aulas for alterada
document.getElementById("quantidadeAulas").addEventListener("change", atualizarTabela);
atualizarTabela();


