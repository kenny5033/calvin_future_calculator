const interestInput = document.getElementById("interestInput");
const funMessages = document.getElementById("funMessages")
const result = document.getElementById("result");
const prereqResult = document.getElementById("prereqResult");

// Many messages generated by ChatGPT
const messages = [
"Your wildest dreams are about to come true...", 
"Your future, only decided by us!",
"Hang tight! We're sprinkling some digital magic ✨",
"Hold on to your hats! Something wonderful is brewing 🎩☕",
"Stay tuned! Our digital elves are hard at work 🧝‍♂️✨",
"Keep calm and wait just a bit longer! Good things come to those who wait ⏳",
"Sit back, relax, and enjoy the anticipation! We're cooking up something special 🍳",
"Inhale patience, exhale excitement! The grand reveal is just around the corner 🎉",
"Brace yourself for awesomeness! We're polishing the final touches ✨💼",
"Keep your eyes on the prize! We're chasing rainbows to bring you something fantastic 🌈",
"Hold on tight! Our code monkeys are typing furiously 🐒🖥️",
"Keep the faith! Our digital hamsters are running as fast as they can 🐹💨"
]

const displayFunMessage = () => {
    // random from array computation mostly from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
    funMessages.textContent = messages[Math.floor(Math.random() * messages.length)];
}

interestInput.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        interestInput.disabled = true; // stop the user from inputting while the server is computing

        /* setup */
        result.textContent = "";

        /* ✨fun✨ */
        displayFunMessage(); // call at once to not wait for first 5000
        const funMessagesInterval = setInterval(displayFunMessage, 4000);

        const interest = interestInput.value;
        fetch('/postInterest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ interestEntry: interest })
        })
        .then(response => {
            if (response.ok) {
                // result.textContent = 'Data successfully submitted!\n';
                return response.text();
            } else {
                result.textContent = 'Failed to submit data!';
            }
        })
        .then(response => {
            response = JSON.parse(response);
            result.innerHTML = `\
            <p>Your recommened classes are</p>\
            <p><button class=btn onclick=getPrereqs(this.innerHTML)>${response.top_choice}</button></p>\
            <p><button class=btn onclick=getPrereqs(this.innerHTML)>${response.second_choice}</button></p>\
            <p><button class=btn onclick=getPrereqs(this.innerHTML)>${response.third_choice}</button></p>`;
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            // once everything, success or failure, has happened return control to user and clean up
            clearInterval(funMessagesInterval);
            interestInput.disabled = false; // allow the user access again
        })   
    }
});

const getPrereqs = target => {
    const targetCourse = target;
    fetch('/postPrereqs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ target: targetCourse })
    })
    .then(response => {
        if (response.ok) {
            // result.textContent = 'Data successfully submitted!\n';
            return response.text();
        } else {
            prereqResult.textContent = 'Failed to submit data!';
        }
    })
    .then(response => {
        response = JSON.parse(response);
        // display the response prettily
        prereqResult.innerHTML = JSON.stringify(response, null, 4);
    })
    .catch(error => {
        console.error('Error:', error);
    })
}