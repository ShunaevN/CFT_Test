const regForm = document.querySelector('.registration__form');
const button = document.querySelector('.intrance_button');

regForm.addEventListener('submit',async (e)=>{
            e.preventDefault();
            const URL = "http://127.0.0.1:8000/auth/register";
            const formData = new FormData(regForm);
            regForm.reset();
            let options = {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(
                {
                      "email": formData.get('email'),
                      "password": formData.get('password'),
                      "is_active": true,
                      "is_superuser": false,
                      "is_verified": false,
                      "name": formData.get('name'),
                      "surname": formData.get('surname')
                    }
              ),
    };
    fetch(URL, options).then(res => res.json()).then(res => console.log(res))
        })
        

        
button.addEventListener('click', (e) => {
    location.href = 'login.html';
    button.removeEventListener();
});
        