function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return null;
    }

document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll(".fa-hand-o-up");

    likeButtons.forEach(button => {

        button.addEventListener("click", function () {

            const imageId = this.dataset.imageId;

            const base_url = 'http://localhost:8000/api/like'

            fetch(`${base_url}/${imageId}`, {
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
})
