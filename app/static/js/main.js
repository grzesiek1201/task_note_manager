// Funkcje do obsługi modali
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Zamykanie modalu po kliknięciu poza nim
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Funkcje do obsługi zadań
function toggleTaskComplete(taskId) {
    fetch(`/tasks/${taskId}/complete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
            if (taskElement) {
                taskElement.classList.toggle('completed');
                const completeButton = taskElement.querySelector('.btn-success, .btn-warning');
                if (completeButton) {
                    if (taskElement.classList.contains('completed')) {
                        completeButton.className = 'btn btn-warning';
                        completeButton.textContent = '↩';
                    } else {
                        completeButton.className = 'btn btn-success';
                        completeButton.textContent = '✓';
                    }
                }
            }
        } else {
            alert('Wystąpił błąd podczas aktualizacji zadania');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Wystąpił błąd podczas aktualizacji zadania');
    });
}

function deleteTask(taskId) {
    if (confirm('Czy na pewno chcesz usunąć to zadanie?')) {
        fetch(`/tasks/${taskId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
                if (taskElement) {
                    taskElement.remove();
                }
                window.location.reload();
            } else {
                alert('Wystąpił błąd podczas usuwania zadania');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Wystąpił błąd podczas usuwania zadania');
        });
    }
}

function editTask(taskId) {
    const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
    if (taskElement) {
        const title = taskElement.querySelector('.item-title').textContent;
        const description = taskElement.querySelector('.item-description').textContent;
        const categoryId = taskElement.getAttribute('data-category-id');
        const dueDate = taskElement.getAttribute('data-due-date');
        const priority = taskElement.getAttribute('data-priority');
        
        const form = document.getElementById('editTaskForm');
        form.action = `/tasks/${taskId}/edit`;
        
        document.getElementById('edit_task_id').value = taskId;
        document.getElementById('edit_task_title').value = title;
        document.getElementById('edit_task_description').value = description;
        document.getElementById('edit_task_category').value = categoryId || '';
        document.getElementById('edit_task_due_date').value = dueDate || '';
        document.getElementById('edit_task_priority').value = priority || 'normal';
        
        showModal('editTaskModal');
    }
}

// Funkcje do obsługi notatek
function deleteNote(noteId) {
    if (confirm('Czy na pewno chcesz usunąć tę notatkę?')) {
        fetch(`/notes/${noteId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                const noteElement = document.querySelector(`[data-note-id="${noteId}"]`);
                if (noteElement) {
                    noteElement.remove();
                }
                window.location.reload();
            } else {
                alert('Wystąpił błąd podczas usuwania notatki');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Wystąpił błąd podczas usuwania notatki');
        });
    }
}

function editNote(noteId) {
    const noteElement = document.querySelector(`[data-note-id="${noteId}"]`);
    if (noteElement) {
        const title = noteElement.querySelector('.item-title').textContent;
        const content = noteElement.querySelector('.item-content').textContent;
        const categoryId = noteElement.getAttribute('data-category-id');
        
        const form = document.getElementById('editNoteForm');
        form.action = `/notes/${noteId}/edit`;
        
        document.getElementById('edit_note_id').value = noteId;
        document.getElementById('edit_note_title').value = title;
        document.getElementById('edit_note_content').value = content;
        document.getElementById('edit_note_category').value = categoryId || '';
        
        showModal('editNoteModal');
    }
}

// Funkcje do obsługi kategorii
function deleteCategory(categoryId) {
    if (confirm('Czy na pewno chcesz usunąć tę kategorię?')) {
        fetch(`/categories/${categoryId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (response.ok) {
                const categoryElement = document.querySelector(`[data-category-id="${categoryId}"]`);
                if (categoryElement) {
                    categoryElement.remove();
                }
                window.location.reload();
            } else {
                alert('Wystąpił błąd podczas usuwania kategorii');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Wystąpił błąd podczas usuwania kategorii');
        });
    }
} 