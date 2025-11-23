
document.addEventListener("DOMContentLoaded", function() {
    const items = document.querySelectorAll('.instruction-item');
    items.forEach((item, index) => {
        item.style.animation = `slideInPlank 0.5s ease-out ${index * 0.15}s forwards`;
    });
});