function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

document.addEventListener("DOMContentLoaded", function () {
    const domain = window.location.origin;

    const likeButtons = document.querySelectorAll(".fa-hand-o-up");
    likeButtons.forEach(button => {

        button.addEventListener("click", function () {

            const imageId = this.dataset.imageId;


            fetch(`${domain}/api/post/${imageId}/like/`, {
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
                    console.log(error)
                })
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
                    "text": inputElement.value
                }

                fetch(`${domain}/api/post/${imageId}/comment/add/`, {
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

                        const userLink = document.createElement('a');
                        userLink.href = `/user-details/${data.user.id}/`;

                        let userImage
                        const imageLink = String(data.user.profile.image)

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


                        userLink.appendChild(userImage);

                        const username = document.createElement('strong');
                        username.textContent = data.user.username;
                        userLink.appendChild(username);


                        const commentTextContainer = document.createElement('div');
                        commentTextContainer.classList.add('comment-text');

                        const commentTextP = document.createElement('p');
                        commentTextP.textContent = data.text
                        commentTextContainer.appendChild(commentTextP);

                        const commentCreatedAt = document.createElement('div');
                        commentCreatedAt.classList.add('comment-created-at');
                        commentCreatedAt.textContent = data.created_at;

                        listItem.appendChild(userLink);
                        listItem.appendChild(commentTextContainer);
                        listItem.appendChild(commentCreatedAt);

                        const commentListElement = document.getElementById(`comment-list-${imageId}`)

                        commentListElement.append(listItem)
                        commentListElement.scrollIntoView({ behavior: "smooth", block: "end" });
                    })
                    .catch(e => {
                        inputElement.value = ''
                    })
            }
        })
    })
})
