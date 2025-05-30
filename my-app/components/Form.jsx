import React, { useEffect } from 'react'


function handleSubmit(event) {

  event.preventDefault();
  console.log(event.target.fname.value);
  console.log(event.target.age.value);
  let userData = {
    name: event.target.fname.value,
    age: event.target.age.value
  }
  
  // submit a post request to the server
  fetch('http://localhost:8000/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  }).then(response => {
    if (response.ok) {
      console.log('Data submitted successfully');
      console.log(response.json());
    } else {
      console.error('Error submitting data');
    }
  }).catch(error => {
    console.error('Error:', error);
  });


}

const Form = () => {
  return (
    <div>
        <form onSubmit={handleSubmit} method="POST">
            <label>Fname: </label>
            <input type="text" name="fname" />
            <label>Age: </label>
            <input type="number" name="age" />
            <input type="submit" value="Submit" />
        </form>
    </div>
  )
}

export default Form