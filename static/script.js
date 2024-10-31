function confirmComplete(taskTitle) {
    return confirm(`Are you sure you want to mark "${taskTitle}" as completed?`);
}

function confirmDelete(taskTitle) {
    return confirm(`Are you sure you want to delete "${taskTitle}"?`);
}
