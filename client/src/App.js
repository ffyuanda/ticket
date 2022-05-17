import React, {useState} from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

const validationSchema = yup.object({
  email: yup
    .string('Enter your email')
    .email('Enter a valid email')
    .required('Email is required'),
});

const TicketResult = (props) => {
  return(
    <div className='TicketResult'>
      <p id='email'>Email: {props.email}</p>
      <div id='dates'>
        <p>Subscribed Dates</p>
        <ul>

        </ul>
      </div>
    </div>
  );
}

const TicketForm = (props) => {

  const [dates, setDates] = useState([]);
  const formik = useFormik({
    initialValues: {
      email: '',
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      props.setEmail(values.email);
      let data = {email: values.email};

      fetch("http://localhost:5000/retrieve", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      }).then(res => {
        console.log("Response:", res)
      });
      // alert(JSON.stringify(values, null, 2));
    },
  });

  return (
    <div className='TicketForm'>
		<h2>SK to HKA Ticket Tracker</h2>
      <form onSubmit={formik.handleSubmit}>
        <TextField
          fullWidth
          id="email"
          name="email"
          label="Email"
          value={formik.values.email}
          onChange={formik.handleChange}
          error={formik.touched.email && Boolean(formik.errors.email)}
          helperText={formik.touched.email && formik.errors.email}
        />
        <Button color="primary" variant="contained" fullWidth type="submit">
          Submit
        </Button>
      </form>
    </div>
  );
};


const App = () => {

  const [email, setEmail] = useState('');

  return(
    <div>
      <TicketForm setEmail={setEmail}/>
      {/* {if (email) {}} */}
      <TicketResult email={email}/>
    </div>
  );
}

export default App;
