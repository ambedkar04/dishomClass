// Admin list view tweaks for CustomUser

document.addEventListener('DOMContentLoaded', function () {
  try {
    const table = document.querySelector('table#result_list');
    if (!table) return;

    // Make each row clickable using first link in the row
    Array.from(table.querySelectorAll('tbody tr')).forEach((tr) => {
      const firstLink = tr.querySelector('a');
      if (!firstLink) return;
      tr.style.cursor = 'pointer';
      tr.addEventListener('click', (e) => {
        // Avoid hijacking clicks on checkboxes or action selects
        const t = e.target;
        if (t instanceof HTMLInputElement || t instanceof HTMLSelectElement || (t && t.closest('a'))) return;
        window.location.href = firstLink.getAttribute('href');
      });
    });

    // Add a subtle badge to inactive rows
    Array.from(table.querySelectorAll('tbody tr')).forEach((tr) => {
      const isActiveCell = tr.querySelector('td.field-is_active');
      if (!isActiveCell) return;
      const hasNoIcon = !!isActiveCell.querySelector('img[src*="icon-no"]');
      if (hasNoIcon) {
        tr.style.backgroundColor = '#fff7f7';
      }
    });
  } catch (e) {
    // fail silently
  }
});
