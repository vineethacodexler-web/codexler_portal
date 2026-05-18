document.addEventListener("DOMContentLoaded", function () {

    /* ================= COUNTER ================= */
    document.querySelectorAll('.counter').forEach(counter => {
      const update = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const speed = target / 40;
  
        if (count < target) {
          counter.innerText = Math.ceil(count + speed);
          setTimeout(update, 30);
        } else {
          counter.innerText = target + "+";
        }
      };
      update();
    });
  
    /* ================= AOS ================= */
    if (typeof AOS !== "undefined") {
      AOS.init({
        duration: 1000,
        once: true
      });
    }
  
    /* ================= PARTICLES ================= */
    if (typeof particlesJS !== "undefined" && document.getElementById("particles-js")) {
      particlesJS("particles-js", {
        particles: {
          number: { value: 60 },
          size: { value: 3 },
          move: { speed: 1.2 },
          line_linked: {
            enable: true,
            opacity: 0.2
          }
        },
        interactivity: {
          events: {
            onhover: { enable: true, mode: "repulse" }
          }
        }
      });
    }
  
    /* ================= TYPING EFFECT ================= */
    const text = "Building Powerful Digital Experiences for Growth";
    const textEl = document.getElementById("typingText");
    const underline = document.getElementById("underline");
    const section = document.getElementById("aboutSection");
  
    let hasStarted = false;
  
    if (textEl && underline && section) {
      window.addEventListener("scroll", () => {
  
        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight;
  
        if (rect.top < windowHeight && rect.bottom > 0) {
          hasStarted = true;
        }
  
        if (!hasStarted) return;
  
        let progress = (windowHeight - rect.top) / rect.height;
        progress = Math.max(0, Math.min(1, progress));
  
        const length = Math.floor(progress * text.length);
  
        textEl.innerHTML = text.substring(0, length);
        underline.style.width = (progress * 100) + "%";
  
      });
    }
  
    /* ================= MOBILE MENU ================= */
    const menuBtn = document.getElementById("menuBtn");
    const mobileMenu = document.getElementById("mobileMenu");
  
    if (menuBtn && mobileMenu) {
      menuBtn.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
      });
    }
  
    /* ================= FADE UP SCROLL ================= */
    const elements = document.querySelectorAll('.fade-up');
  
    window.addEventListener('scroll', () => {
      elements.forEach(el => {
        const top = el.getBoundingClientRect().top;
        if (top < window.innerHeight - 50) {
          el.classList.add('active');
        }
      });
    });
  
    /* ================= FAQ TOGGLE ================= */
    document.querySelectorAll('.faq-question').forEach(button => {
      button.addEventListener('click', () => {
        const item = button.parentElement;
        item.classList.toggle('active');
      });
    });
  
  });