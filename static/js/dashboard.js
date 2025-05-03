// Gestion du toggle du sidebar
document.addEventListener('DOMContentLoaded', function() {
  const sidebar = document.querySelector('.sidebar');
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  
  // Toggle sidebar
  if (sidebarToggleBtn) {
      sidebarToggleBtn.addEventListener('click', function() {
          sidebar.classList.toggle('show');
          sidebarOverlay.classList.toggle('active');
      });
  }
  
  // Fermer le sidebar quand on clique sur l'overlay
  if (sidebarOverlay) {
      sidebarOverlay.addEventListener('click', function() {
          sidebar.classList.remove('show');
          this.classList.remove('active');
      });
  }
  
  // Initialisation des dropdowns Bootstrap
  document.querySelectorAll('.dropdown-toggle').forEach(function(element) {
      new bootstrap.Dropdown(element);
  });
});



