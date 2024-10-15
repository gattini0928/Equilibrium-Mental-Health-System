document.querySelector('.dropdown-btn').addEventListener('click', function() {
    const dropdownList = document.querySelector('.dropdown-list');
    // Alterna entre mostrar ou esconder a lista
    dropdownList.style.display = dropdownList.style.display === 'flex' ? 'none' : 'flex';
});


// Função para filtrar a lista de itens com base no texto digitado
function filterItems() {
    const input = document.getElementById('searchBar');
    const filter = input.value.toLowerCase();
    const ul = document.getElementById('dropdownList');
    const li = ul.getElementsByTagName('li');
    
    ul.style.display = "flex"; // Mostrar o dropdown quando começar a digitar
    
    // Loop através dos itens e ocultar os que não correspondem à pesquisa
    for (let i = 0; i < li.length; i++) {
        const item = li[i].textContent || li[i].innerText;
        if (item.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

// Função para selecionar o item da lista
function selectItem(element) {
    const input = document.getElementById('searchBar');
    input.value = element.innerText; // Definir o valor do input como o texto do item selecionado
    document.getElementById('dropdownList').style.display = "none"; // Esconder o dropdown
}
