const fullName = document.getElementById('full-name-input')
const city = document.getElementById('city-input')
const address = document.getElementById('address-input')
const email = document.getElementById('email-input')
const phoneNumber = document.getElementById('phone-number-input')

const errMessage = document.getElementById('warning')




const form = document.getElementById('visitor-registration')


form.addEventListener('change', (e) => {
    message = []

   const possibleFullName = fullName.value.split(' ')
   if(possibleFullName.length > 0 && possibleFullName.length < 2 ){
        e.preventDefault()
       fullName.style.borderBottom = "1px solid red"
       message.push("Full Name")
   }

   if(city.value.length > 0 && city.value.length < 3){
        e.preventDefault()
        city.style.borderBottom = "1px solid red"
        message.push("City")
    }

    if(address.value.length > 0 && address.value.length < 5){
        e.preventDefault()
        address.style.borderBottom = "1px solid red"
        message.push("Address")
    }


    if(email.value.length > 0 && email.value.length < 5){
        e.preventDefault()
        email.style.borderBottom = "1px solid red"
        message.push("Email")
    }
    


    if(phoneNumber.value.length > 0 && phoneNumber.value.length < 5){
        e.preventDefault()
        phoneNumber.style.borderBottom = "1px solid red"
        message.push("Phone Number")
    }


   
   errMessage.innerText = "Valid " + message.join(", ") + " is/are required."

})