function completeAssessment(id) {
    console.log("Marking assessment " + id + " as complete.");
}

function deleteAssessment(id) {
    console.log("Deleting assessment " + id + ".");
}

function unfinishAssessment(id) {
    console.log("Marking assessment " + id + " as uncomplete.");
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');

    if (form) {
        form.addEventListener('submit', function (event) {
            const deadline = document.getElementById('deadline_date').value;

            const now = new Date();
            const deadlineDate = new Date(deadline);

            if (deadlineDate < now) {
                alert("Deadline must be in the future.");
                event.preventDefault();
            }
        });
    }
});