function confirmComplete(taskTitle) {
    return confirm(`Are you sure you want to mark "${taskTitle}" as completed?`);
}

function confirmDelete(taskTitle) {
    return confirm(`Are you sure you want to delete "${taskTitle}"?`);
}

function filterTasks(status) {
    const tasks = document.querySelectorAll('.list-group-item');
    tasks.forEach(task => {
        if (status === 'all' || task.getAttribute('data-status') === status) {
            task.style.display = 'block';
        } else {
            task.style.display = 'none';
        }
    });
}

function searchTasks() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    document.querySelectorAll('.list-group-item').forEach(task => {
        const title = task.querySelector('h5').textContent.toLowerCase();
        const description = task.querySelector('small').textContent.toLowerCase();
        task.style.display = title.includes(query) || description.includes(query) ? 'block' : 'none';
    });
}

function allowDrop(event) {
    event.preventDefault();
}

function dragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.id);
}

function drop(event) {
    event.preventDefault();
    const draggedId = event.dataTransfer.getData("text/plain");
    const draggedElement = document.getElementById(draggedId);
    event.target.closest('.list-group').insertBefore(draggedElement, event.target);
}

function updateProgressBar() {
    const tasks = document.querySelectorAll('.list-group-item');
    const completedTasks = document.querySelectorAll('.list-group-item[data-status="completed"]');
    const progress = tasks.length ? Math.round((completedTasks.length / tasks.length) * 100) : 0;
    const progressBar = document.getElementById("taskProgressBar");
    progressBar.style.width = progress + '%';
    progressBar.textContent = progress + '%';
}

document.addEventListener('DOMContentLoaded', updateProgressBar);
