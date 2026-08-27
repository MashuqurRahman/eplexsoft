function scrollToForm() {
  document.getElementById('formSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  const nameInput = document.getElementById('bName');
  if (nameInput) nameInput.focus();
}

function cancelEdit() {
  // edit mode is driven by the ?edit=<id> query param; dropping it resets the form
  window.location.href = window.location.pathname;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function confirmDeleteBranch(form, branchName) {
  Swal.fire({
    title: 'Remove branch?',
    html: `This will remove <strong>${escapeHtml(branchName)}</strong>. This cannot be undone.`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Remove',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#c0392b',
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      form.submit();
    }
  });
}

function showToast(msg) {
  const t = document.getElementById('toast');
  document.getElementById('toastMsg').textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

document.addEventListener('DOMContentLoaded', () => {
  if (window.SERVER_TOAST) {
    showToast(window.SERVER_TOAST);
  }
});