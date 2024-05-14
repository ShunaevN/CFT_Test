export let token = '091745e2-6558-4920-8a4c-5cb3a3684e8a';
const form = document.querySelector('.entrance__form');
const entranceButton = document.querySelector('.intrance_button');
const backButton = document.querySelector('.back_button');

backButton.addEventListener('click', (e) => {
            e.preventDefault();
            location.href = 'registration.html';
           
});

entranceButton.addEventListener('click', async (e)=>{
            e.preventDefault();
            const URL = "http://127.0.0.1:8000/login";
            const formData = new FormData(form);
            let options = {

              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(
                {     
                      "email": formData.get('email'),
                      "password": formData.get('password'),
                }),

              };

            fetch(URL, options)
              .then(res => res.json())
              .then(data => {
                if (data["token"]){
                  localStorage.setItem("token", data["token"]);
                  localStorage.setItem("user_id", data["user_id"]);
                  location.href = 'profile.html';
                }
                })
                .catch(error => {console.error(error)});
                
    })
