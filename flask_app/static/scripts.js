const sideMenu = document.querySelector('aside')
const menuBtn = document.querySelector('#menu-btn')
const closeBtn = document.querySelector('#close-btn')
const themeToggler = document.querySelector('.theme-toggler')
const sidebarLinks = document.querySelectorAll(".sidebar a");
// show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

// close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

// change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
})



// sidebarLinks.forEach( link => {
//     link.addEventListener("click", function() {
//     // Remove the "active" class from all links
//         sidebarLinks.forEach(link => {
//             link.classList.remove("active");
//         });

//     // Add the "active" class to the clicked link
//         this.classList.add("active");
//     });
// });
