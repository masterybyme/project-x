import { useState, useEffect } from "react";
import { useTheme, Box, Button, TextField, InputAdornment, MenuItem, Select, FormControl, InputLabel, Snackbar, Typography  } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";
import { tokens } from "../../theme";
import axios from 'axios';


const Company = ({ company }) => {
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const [showSuccessNotification, setShowSuccessNotification] = useState(false);
  const [showErrorNotification, setShowErrorNotification] = useState(false);
  const theme = useTheme();
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");
  const colors = tokens(theme.palette.mode);

  useEffect(() => {
    fetchData();
  }, []);

  //Datafetch for User-Display in Team.jsx
  async function fetchData() {
    try {
      const response = await axios.get("http://localhost:5000/api/company");
      const data = response.data;
      setUsers(data);
    } catch (error) {
      console.error("Error fetching data:", error.response ? error.response : error);
      setMessage("An error occurred while fetching data.");
    }
  }

  const handleFormSubmit = (values, { resetForm }) => {
    axios
      .post('http://localhost:5000/api/company', values)
      .then((response) => {
        console.log(response.data);
        setShowSuccessNotification(true);
        resetForm();
      })
      .catch((error) => {
        console.error(error);
        setShowErrorNotification(true);
      });
  };

  return (
    <Box m="20px">
      <Header title="COMPANY" 
      subtitle="Please update your company data whenever necessary. This are the basics for your optimized Scheduler." 
      />
      <h2>Company Information</h2>

      <Formik
        onSubmit={handleFormSubmit}
        initialValues={initialValues}
        validationSchema={checkoutSchema}
      >
        {({
          values,
          errors,
          touched,
          handleBlur,
          handleChange,
          handleSubmit,
        }) => (
          <form onSubmit={handleSubmit}>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(6, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 6" },
              }}
            >
            <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "right",
                height: "100%",
                }}>
             Firmennamen
            </Typography>
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Company Name"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.first_name}
                name="company_name"
                error={!!touched.first_name && !!errors.first_name}
                helpertext={touched.first_name && errors.first_name}
                sx={{ gridColumn: "span 1" }}
              />
              <Typography color={colors.greenAccent[500]} variant="" sx={{
                gridColumn: "span 4",
                display: "grid",
                alignItems: "center",
                height: "100%",
                }}>
            </Typography>
              <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "right",
                height: "100%",
                }}>
             Weekly Hours
            </Typography>
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Hour"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.last_name}
                name="weekly_hour"
                error={!!touched.last_name && !!errors.last_name}
                helpertext={touched.last_name && errors.last_name}
                sx={{ gridColumn: "span 1" }}
              />
              <Typography color={colors.greenAccent[500]} variant="" sx={{
                gridColumn: "span 4",
                display: "grid",
                alignItems: "center",
                height: "100%",
                }}>
            </Typography>
              <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "right",
                height: "100%",
                }}>
             Shifts
            </Typography>
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="No. of Shifts"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.email}
                name="shift"
                error={!!touched.email && !!errors.email}
                helpertext={touched.email && errors.email}
                sx={{ gridColumn: "span 1" }}
              />
              <Typography color={colors.greenAccent[500]} variant="" sx={{
                gridColumn: "span 4",
                display: "grid",
                alignItems: "center",
                height: "100%",
                }}>
            </Typography>
            </Box>
            <></>
            <></>
            <h2>Opening Hour</h2>
            <></>
            <></>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(6, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 6" },
              }}
            >
              <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "center",
                height: "100%",
                }}>
             Weekday
            </Typography>
            <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "center",
                height: "100%",
                }}>
             Start Time
            </Typography>
            <Typography color={colors.greenAccent[500]} variant="h6" sx={{
                gridColumn: "span 1",
                display: "flex",
                alignItems: "center",
                height: "100%",
                }}>
             End Time
            </Typography>
            <Typography color={colors.greenAccent[500]} variant="" sx={{
                gridColumn: "span 3",
                display: "flex",
                alignItems: "center",
                height: "100%",
                }}>
            </Typography>
              {Array.from({ length: 7 }).map((_, rowIndex) => (
                <>
                <Typography
                  key={`number-${rowIndex}`}
                  color={colors.greenAccent[500]}
                  variant=""
                  sx={{
                    gridColumn: "span 1",
                    display: "flex",
                    alignItems: "center",
                    height: "100%",
                  }}
                >
                 {[rowIndex]}
                  </Typography>
                  <TextField
                    key={`day_${rowIndex}_0`}
                    fullWidth
                    variant="filled"
                    type="time"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    value={`${rowIndex + 1}0`}
                    name={`start_time_${rowIndex}`}
                    error={!!touched[`start_time_${rowIndex}`] && !!errors[`start_time_${rowIndex}`]}
                    helperText={touched[`start_time_${rowIndex}`] && errors[`start_time_${rowIndex}`]}
                    sx={{ gridColumn: "span 1" }}
                  />
                  <TextField
                    key={`day_${rowIndex}_1`}
                    fullWidth
                    variant="filled"
                    type="time"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    value={`${rowIndex + 1}1`}
                    name={`end_time_${rowIndex}`}
                    error={!!touched[`end_time_${rowIndex}`] && !!errors[`end_time_${rowIndex}`]}
                    helperText={touched[`end_time_${rowIndex}`] && errors[`end_time_${rowIndex}`]}
                    sx={{ gridColumn: "span 1" }}
                  />
                  <Typography
                    key={`empty-1-${rowIndex}`}
                    color={colors.greenAccent[500]}
                    variant=""
                    sx={{
                      gridColumn: "span 3",
                      display: "flex",
                      alignItems: "center",
                      height: "100%",
                    }}
                  ></Typography>
                  
                </>
              ))}
            </Box>
            <Box display="flex" justifyContent="end" mt="20px">
              <Button type="submit" color="secondary" variant="contained">
                Update
              </Button>
            </Box>
          </form>
        )}
      </Formik>
      <Snackbar
        open={showSuccessNotification}
        onClose={() => setShowSuccessNotification(false)}
        message="Registration successful"
        autoHideDuration={3000}
        sx={{
          backgroundColor: "green !important", 
          color: "white", 
          "& .MuiSnackbarContent-root": {
            borderRadius: "4px",
            padding: "15px",
            fontSize: "16px",
          },
        }}
      />
      <Snackbar
        open={showErrorNotification}
        onClose={() => setShowErrorNotification(false)}
        message="Error occurred - Your email might already be in use"
        autoHideDuration={3000}
        sx={{
          backgroundColor: "red !important", 
          color: "white", 
          "& .MuiSnackbarContent-root": {
            borderRadius: "4px",
            padding: "15px",
            fontSize: "16px",
          },
        }}
      />

    </Box>
  );
};


const checkoutSchema = yup.object().shape({
  first_name: yup.string().required("required"),
  last_name: yup.string().required("required"),
  email: yup.string().email("invalid email").required("required"),
  password: yup.string().required("required"),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref("password"), null], "Passwords must match")
    .required("required"),
  company_name: yup.string().required("required"),
  access_level: yup.string().required("required"),
  employment_level: yup
    .number()
    .min(0, 'Company level must be greater than or equal to 0%')
    .max(100, 'Company level must be less than or equal to 100%')
    .required("required"),
});

const initialValues = {
  first_name: "",
  last_name: "",
  email: "",
  employment_level: "",
  company_name: "company_name",
  access_level: "",
  department: "",
  password: "",
  confirmPassword: "",
  10:"10"
  
};

export default Company;
