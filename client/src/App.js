import React, {useState, useEffect} from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';

const validationSchema = yup.object({
  email: yup
    .string('Enter your email')
    .email('Enter a valid email')
    .required('Email is required'),
});

const dateSchema = yup.string().matches(/^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$/);

const AddDate = (props) => {
 
  const [date, setDate] = useState('');
  const [error, setError] = useState(null)

  async function handleClick() {
    const result = await dateSchema.isValid(date);
    if (!result) {
      setError(true);
      return;
    }
    else
      setError(false);

    if (props.email && result) {

      let data = {
        email: props.email,
        date: date,
      }

      fetch("http://localhost:5000/register", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      }).then(res => res.json())
      .then(res => {
        if (res['result'] == 'OK')
          props.setReloadCount(!props.reloadCount)
      });
    }
  }

  const handleChange = (event) => {
    setDate(event.target.value);
  }

  return (
    <Stack direction="row" spacing={1}
      alignItems="flex-center" sx={{
      marginLeft: "2%",
      marginTop: "1.1%",
    }}>

      <TextField id="add_date" label="Date (yyyy-mm-dd)" variant="outlined" sx={{
      display: "inline",
      }} size="small" onChange={handleChange} 
      error={error}
      />

      <Button color="primary" 
      variant="contained" 
      onClick={handleClick}
      >Add</Button>

    </Stack>
    
  );

}

const DateButton = (props) => {

  return (
    <Grid item xs={6} sm={3}>
      <Button variant="contained" size='small'>{props.date}</Button>  
    </Grid>
  );
}


const DatesPanel = (props) => {

  let [dates, setDates] = useState([]);
  let [DateButtons, setDateButtons] = useState([]);
  
  const getDates = () => {
    if (props.email) {

      let data = {
        email: props.email,
      }
  
      fetch("http://localhost:5000/dates", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      }).then(res => res.json())
      .then(
        res => {
          let _dates = res['dates'];
          setDates(_dates);
        }
      );

    }
  };

  const getDateButtons = () => {
    let DateButtonArray = [];
    for (let i = 0; i < dates.length; i++) {
      DateButtonArray.push(<DateButton key={i} date={dates[i]}></DateButton>);
    }
    setDateButtons(DateButtonArray);
  }

  useEffect(getDates, [props.email, props.reloadCount]);
  useEffect(getDateButtons, [dates]);

  return (
    <div id='dates'>
        <p className='center'>Subscribed Dates</p>
        <Grid container spacing={1} sx={{
          textAlign: 'center',
        }}>
          {DateButtons}
        </Grid>
    </div>
  );

}

const TicketResult = (props) => {
  let [reloadCount, setReloadCount] = useState(true);

  return(
    <div className='TicketResult'>
      <p id='email'>Email: {props.email}</p>
      <AddDate email={props.email} 
      reloadCount={reloadCount}
      setReloadCount={setReloadCount}/>
      <DatesPanel email={props.email} reloadCount={reloadCount}/>
    </div>
  );
}

const TicketForm = (props) => {

  const formik = useFormik({
    initialValues: {
      email: '',
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      
      let data = {email: values.email};

      fetch("http://localhost:5000/retrieve", {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
      }).then(res => {
        props.setEmail(values.email);
        console.log("Response:", res)
      });

    },
  });

  return (
    <div className='TicketForm'>
		<h3>SK to HKA Ticket Tracker</h3>

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
  let ticketResult;
  if (email && email != '')
    ticketResult = <TicketResult email={email}/>;
  else
    ticketResult = null;

  return(
    <div>
      <TicketForm setEmail={setEmail}/>
      {ticketResult}
    </div>
  );
}

export default App;
