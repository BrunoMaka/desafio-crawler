function toggleMenu() {
    const menu = document.querySelector('.menu');
    const pages = document.querySelectorAll('.page-container');
    menu.classList.toggle('expanded');
    
    if (menu.classList.contains('expanded')) {
        pages.forEach(page => {
            page.classList.add('menu-expanded');
        });
    } else {
        pages.forEach(page => {
            page.classList.remove('menu-expanded');
        });
    }
}    