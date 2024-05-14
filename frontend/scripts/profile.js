const button = document.querySelector('.profile_button');
const userSalary = document.querySelector('.user_salary');
const userNextGrade = document.querySelector('.user_next_grade');
const userWelcome = document.querySelector('.title');

const userName = document.querySelector('.user_name');
const userSurname = document.querySelector('.user_surname');
const userEmail = document.querySelector('.user_email');

const userInfo = document.querySelector('.about_user');

fetch(`http://127.0.0.1:8000/profile/${localStorage.getItem("user_id")}`, {
            headers: {
                "Content-Type": 'application/json',
                "Authorization": `${localStorage.getItem("token")}`
                }
        })
        .then(response => response.json())
        .then(data => {
                userWelcome.textContent = `Добро пожаловать, ${data.name}!`;
                userSalary.textContent = `Текущая зарплата сотрудника: ${data.Salary} рублей.`;
                userNextGrade.textContent = 
                        `Следующее повышение: ${data.Next_grade_data.split('T')[0]}`;
                userName.textContent = `Имя: ${data.name}`;
                userSurname.textContent = `Фамилия: ${data.surname}`;
                userEmail.textContent = `Эл. почта: ${data.email}`;
            });

button.addEventListener('click', async (e)=>{
        e.preventDefault();
        if (button.textContent === 'Показать критически важные данные'){
                userInfo.style.display = 'flex';
                button.textContent = 'Скрыть критически важные данные';
        }
        else {
                userInfo.style.display = 'none';
                button.textContent = 'Показать критически важные данные';
        }
 
    });