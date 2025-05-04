// sidebar.js
function scrollToSection(id) {
    const el = document.getElementById(id);
    if (!el) return;
  
    const elementTop = el.getBoundingClientRect().top + window.scrollY;
    const scrollTarget = elementTop - (window.innerHeight / 2) + (el.offsetHeight / 2);
  
    window.scrollTo({
      top: scrollTarget,
      behavior: 'smooth'
    });
  }
  