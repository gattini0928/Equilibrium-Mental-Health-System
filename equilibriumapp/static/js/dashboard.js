function toggleDropdown(event) {
    const dropdown = event.target.closest('.dropdown').querySelector('.dropdown-list');
    dropdown.classList.toggle('show');
}