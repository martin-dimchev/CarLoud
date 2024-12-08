function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

const domain = window.location.origin;

//Edit button event listener:
function editButtonEventListener(editButton) {
    editButton.addEventListener('click', function () {
        const commentItem = this.closest('li');
        const commentId = commentItem.dataset.commentId;
        const commentTextElement = commentItem.querySelector('.comment-text p');
        const originalText = commentTextElement.textContent.trim();


        const textarea = document.createElement('textarea');
        textarea.classList.add('form-control', 'mt-2', 'comment-edit-area');
        textarea.value = originalText;


        const saveButton = document.createElement('button');
        saveButton.classList.add('btn', 'btn-sm', 'btn-primary', 'save-btn');
        saveButton.innerHTML = '<i class="fa fa-check" aria-hidden="true"></i>'

        // Create Cancel button
        const cancelButton = document.createElement('button');
        cancelButton.classList.add('btn', 'btn-sm', 'btn-primary', 'cancel-btn');
        cancelButton.innerHTML = '<i class="fa fa-times" aria-hidden="true"></i>'

        function cleanupEditForm() {
            textarea.remove();
            saveButton.remove();
            cancelButton.remove();
            commentTextElement.style.display = '';
            editButton.style.display = 'block'
        }

        cancelButton.addEventListener('click', () => {
            cleanupEditForm();
        });

        commentTextElement.style.display = 'none';
        commentItem.querySelector('.comment-text').appendChild(textarea);
        commentItem.querySelector('.comment-text').appendChild(saveButton);
        commentItem.querySelector('.comment-text').appendChild(cancelButton);
        textarea.focus()
        editButton.style.display = 'none';

        saveButton.addEventListener('click', () => {
            const newText = textarea.value.trim();

            if (newText !== '') {
                fetch(`${domain}/api/comments/comment/${commentId}/edit/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({text: newText})
                })
                    .then(response => response.json())
                    .then(data => {
                        commentTextElement.textContent = newText;
                        cleanupEditForm();
                        editButton.style.display = 'block'
                    })
                    .catch(e => {
                        console.log(e)
                    })
            } else {
                cleanupEditForm();
            }
        });
    });
}


//Delete button event listener
function deleteButtonEventListener(deleteButton) {
    const commentId = deleteButton.dataset.commentId

    deleteButton.addEventListener('click', function () {
        fetch(`${domain}/api/comments/comment/${commentId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
            .then(response => {
                if (response.ok) {
                    document.querySelector(`li[data-comment-id="${commentId}"]`).remove();
                }
            })
            .catch(error => console.error('Error:', error));
    })

}

//Comment section logic
document.addEventListener("DOMContentLoaded", function () {

    const likeButtons = document.querySelectorAll(".fa-hand-o-up");

    likeButtons.forEach(button => {

        button.addEventListener("click", function () {

            const imageId = this.dataset.imageId;


            fetch(`${domain}/api/posts/post/${imageId}/like/`, {
                method: "POST",
                credentials: "include",
                referrer: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Content-Type": "application/json",
                },

            })
                .then(response => response.json())
                .then(data => {
                    const likeCounter = this.querySelector(".like-counter");
                    likeCounter.textContent = data.likes_count;
                    if (data.liked) {
                        this.classList.add('liked')
                    } else {
                        this.classList.remove('liked')
                    }

                })
                .catch(error => {
                    console.error('Error liking post:', error);
                });
        });
    });

    const commentAddFormElements = document.querySelectorAll('.comment-add-form')

    commentAddFormElements.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault()
            const inputElement = form.querySelector('input[type="text"]')
            const imageId = this.dataset.imageId;
            if (inputElement.value.trim()) {
                const data = {
                    "text": inputElement.value,
                    "image": imageId
                }

                fetch(`${domain}/api/comments/add/`, {
                    method: "POST",
                    credentials: "include",
                    referrer: "same-origin",
                    headers: {
                        "X-CSRFToken": getCookie('csrftoken'),
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data)
                })
                    .then(response => response.json())
                    .then(data => {
                        inputElement.value = ''
                        const listItem = document.createElement('li');
                        listItem.classList.add('list-group-item');
                        listItem.dataset.commentId = data.id

                        const userLink = document.createElement('a');
                        userLink.href = `/user-details/${data.user.id}/`;
                        console.log(data.user)
                        let userImage
                        const imageLink = data.user.profile && data.user.profile.image
                            ? String(data.user.profile.image)
                            : null;


                        if (imageLink != null) {
                            userImage = document.createElement('img');
                            userImage.src = imageLink;
                            userImage.classList.add('profile-pic');
                        } else {
                            userImage = document.createElement('img');
                            userImage.src = '/static/assets/images/anonymous-user.jpg';
                            userImage.classList.add('profile-pic');
                            userImage.alt = 'profile-pic';
                        }

                        const commentHeaderDivElement = document.createElement("div")
                        commentHeaderDivElement.classList.add('comment-header')

                        userLink.appendChild(userImage);
                        const username = document.createElement('strong');
                        username.textContent = data.user.username;
                        userLink.appendChild(username);

                        const deleteButtonElement = document.createElement('button');
                        deleteButtonElement.classList.add('btn', 'btn-sm', 'btn-danger', 'delete-btn');
                        deleteButtonElement.dataset.commentId = data.id;
                        deleteButtonElement.innerHTML = '<i class="fa fa-trash" aria-hidden="true"></i>';
                        deleteButtonEventListener(deleteButtonElement);

                        commentHeaderDivElement.appendChild(userLink)
                        commentHeaderDivElement.appendChild(deleteButtonElement)

                        const commentTextContainer = document.createElement('div');
                        commentTextContainer.classList.add('comment-text');

                        const commentTextP = document.createElement('p');
                        commentTextP.textContent = data.text
                        commentTextContainer.appendChild(commentTextP);

                        const editButtonElement = document.createElement('button')
                        editButtonElement.classList.add('btn', 'btn-sm', 'btn-link', 'edit-btn')
                        editButtonElement.innerHTML = '<i class="fa fa-pencil" aria-hidden="true"></i>'
                        editButtonEventListener(editButtonElement)
                        commentTextContainer.appendChild(editButtonElement);

                        const commentCreatedAt = document.createElement('div');
                        commentCreatedAt.classList.add('comment-created-at');
                        commentCreatedAt.textContent = data.created_at;

                        listItem.appendChild(commentHeaderDivElement);
                        listItem.appendChild(commentTextContainer);
                        listItem.appendChild(commentCreatedAt);

                        const commentListElement = document.getElementById(`comment-list-${imageId}`)
                        commentListElement.appendChild(listItem)
                        commentListElement.scrollIntoView({behavior: "smooth", block: "end"});
                    })
                    .catch(e => {
                        inputElement.value = ''
                        console.log(e)
                    })
            }
        });
    });

    const commentEditElements = document.querySelectorAll('.edit-btn')
    commentEditElements.forEach(editBtn => {
        editButtonEventListener(editBtn)
    });

    const commentDeleteButtonElements = document.querySelectorAll('.delete-btn')
    commentDeleteButtonElements.forEach(deleteBtn => {
        deleteButtonEventListener(deleteBtn)
    });

    const shareIcons = document.querySelectorAll('.share-icon');

    shareIcons.forEach(icon => {
        icon.addEventListener('click', function () {
            const projectId = this.dataset.projectId;
            const imageId = this.dataset.imageId;

            const postLink = `${domain}/projects/project/${projectId}/images/image/${imageId}`;

            navigator.clipboard.writeText(postLink)
                .then(() => {
                    const feedback = document.createElement('span');
                    feedback.classList.add('copy-feedback');
                    feedback.textContent = 'Copied!';
                    this.parentNode.insertBefore(feedback, this.nextSibling);

                    setTimeout(() => {
                        feedback.remove();
                    }, 1500);
                })
                .catch(error => {
                    console.error('Failed to copy link:', error);
                });
        });
    });

    const followButtonElement = document.querySelector('#follow-btn')

    if (followButtonElement != null) {
        const is_following = followButtonElement.dataset.followId
        followButtonElement.addEventListener('click', function () {
            fetch(`${domain}/api/accounts/account/${is_following}/follow/`, {
                method: "POST",
                credentials: "include",
                referrer: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie('csrftoken'),
                    "Content-Type": "application/json",
                }
            })
                .then(response => response.json())
                .then(data => {
                    const followersCountPElement = document.querySelector('#followers-count')
                    let count = Number(followersCountPElement.textContent)
                    const strongElement = document.createElement('strong')

                    if (data.is_followed === true) {
                        followButtonElement.textContent = 'Follow'
                        count++
                        followersCountPElement.textContent = ''
                        strongElement.textContent = count
                        followersCountPElement.appendChild(strongElement)

                    } else {
                        followButtonElement.textContent = 'Unfollow'
                        count--
                        followersCountPElement.textContent = ''
                        strongElement.textContent = count
                        followersCountPElement.appendChild(strongElement)
                    }
                })
                .catch(errors => console.log(errors))


        })
    }

})


