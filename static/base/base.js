
document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.getElementsByClassName("menu-item");
    const activeIndex = localStorage.getItem('activeIndex');

    if (activeIndex !== null) {
        menuItems[activeIndex].classList.add("active");
    }

    for (let i = 0; i < menuItems.length; i++) {
        menuItems[i].addEventListener('click', function() {
            menuItems[activeIndex].classList.remove("active")
            localStorage.setItem('activeIndex', i);
            menuItems[i].classList.add("active");
        });
    }
});